# Agentic Loop Implementation Plan

## Overview

Building a feedback loop where tool call results (pass or fail) are sent back to the Controller for re-evaluation, enabling the agent to autonomously complete multi-step coding tasks through iterative planning and execution.

---

## Target Architecture

### Current Flow (Linear - Single Pass)
```
User Prompt → Controller → Steps → Tool Caller → Execute → Done
```

### Target Flow (Agentic Loop)
```
User Prompt
     ↓
[Controller] → breaks down request into steps
     ↓
[Tool Caller] → calls tools to execute steps
     ↓
[Execute Tools] → runs read/write/run operations
     ↓
[Loop back to Controller] → results fed back for re-planning
     ↓
... repeat until Controller signals "done"
     ↓
Final Synthesized Output
```

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Loop location | `main.py` | User requested no new modules; keep it centralized |
| Feedback target | **Controller** (not Tool Caller) | All results go to Controller for re-planning — Controller decides next steps |
| Max iterations | **Variable** (`--max-iterations` CLI flag) | Not hardcoded; allows users to tune per task |
| Final output | Synthesized by Controller | Controller produces a final summary after writes are confirmed |

---

## File-by-File Changes

### 1. `prompts.py` — Update Prompts

**Changes:**
- `controllerPrompt`: Add instruction to output a special signal when task is complete (e.g., `[DONE]` tag in response)
- `controllerPrompt`: Add instruction to interpret tool results and decide next steps or signal completion
- `controllerPrompt`: Add instruction to verify write operations succeeded before marking done
- `toolCallerSystemPrompt`: Add instruction to call tools one at a time or in small batches for clarity

**New Controller Prompt fields:**
```
When you receive tool results:
- If steps failed: output revised steps to fix the errors
- If steps succeeded but more steps remain: output next steps
- If all steps complete and writes verified: output [DONE] and a brief summary

Never output [DONE] until you have received confirmation that write/run operations succeeded.
```

---

### 2. `main.py` — Implement the Agentic Loop

**Changes:**

#### (a) CLI Arguments
Add two new CLI arguments:
```
--max-iterations INT   Max loops before forcing stop (default: 50)
--working-dir PATH     Root directory for tool operations (default: '.')
```

#### (b) New Variables
```python
max_iterations = int(sys.argv[sys.argv.index("--max-iterations") + 1]) if "--max-iterations" in sys.argv else 50
working_dir = sys.argv[sys.argv.index("--working-dir") + 1] if "--working-dir" in sys.argv else "."
iteration_count = 0
is_done = False
```

#### (c) Main Loop Structure
```python
# Step 1: Initial planning
controllerChatCompletion = client.chat.completions.create(
    messages=[{"role": "system", "content": controllerPrompt},
              {"role": "user", "content": UserPrompt}],
    model="llama-3.1-8b-instant",
)
controllerSteps = controllerChatCompletion.choices[0].message.content
iteration_count += 1

while not is_done and iteration_count < max_iterations:
    # Step 2: Tool caller executes steps
    toolCallerCompletion = client.chat.completions.create(
        messages=[{"role": "system", "content": toolCallerSystemPrompt},
                  {"role": "user", "content": f"Execute the following steps:\n{controllerSteps}"}],
        tools=toolSchema,
        tool_choice="auto",
        model="llama-3.3-70b-versatile",
    )

    tool_calls = toolCallerCompletion.choices[0].message.tool_calls

    if not tool_calls:
        # No tools called — ask controller for next steps or final output
        controller_input = f"Tool caller took no action. Current steps:\n{controllerSteps}\nWhat should happen next?"
    else:
        # Step 3: Execute tools
        results = run_tool_calls(tool_calls)

        # Step 4: Format results for controller
        formatted_results = format_tool_results(tool_calls, results)

        # Step 5: Feed results back to controller
        controller_input = (
            f"Previous steps:\n{controllerSteps}\n\n"
            f"Tool execution results:\n{formatted_results}\n\n"
            f"Should you revise steps, continue, or mark done? "
            f"If all write/run operations succeeded and no more steps needed, output [DONE]."
        )

    # Step 6: Controller re-evaluates
    controllerChatCompletion = client.chat.completions.create(
        messages=[{"role": "system", "content": controllerPrompt},
                  {"role": "user", "content": controller_input}],
        model="llama-3.1-8b-instant",
    )
    controllerSteps = controllerChatCompletion.choices[0].message.content
    iteration_count += 1

    # Step 7: Check for [DONE] signal
    if "[DONE]" in controllerSteps:
        is_done = True
        final_output = controllerSteps.replace("[DONE]", "").strip()
```

#### (d) New Helper Function: `format_tool_results`
```python
def format_tool_results(tool_calls, results):
    """Format tool call results into a readable string for the controller."""
    output = []
    for tool_call, result in zip(tool_calls, results):
        func_name = tool_call.function.name
        func_args = tool_call.function.arguments
        output.append(f"Tool: {func_name}\nArgs: {func_args}\nResult: {result}\n")
    return "\n".join(output)
```

---

### 3. `functions/run_functions.py` — Preserve `tool_call_id`

**Changes:**
- Modify `run_tool_calls` to return a list of dicts that includes the `tool_call.id` alongside the result
- This is needed so tool results could be properly correlated if needed later

```python
def run_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        name = tool_call.function.name
        try:
            arguments = json.loads(tool_call.function.arguments)
        except Exception:
            arguments = {}

        func = availableFunctions.get(name)
        if not func:
            res = f'Error: Function "{name}" not found'
        else:
            res = func(**arguments)

        results.append({
            "tool_call_id": tool_call.id,
            "function_name": name,
            "result": res
        })

    return results
```

---

### 4. `main.py` — Add Final Output Handling

After the loop exits:
- If `is_done == True`: Print `final_output` (Controller's synthesized summary)
- If `iteration_count >= max_iterations`: Print a "max iterations reached" warning with whatever the last controller output was
- Always print total iterations used

```python
if is_done:
    print(f"\n{'='*50}")
    print("TASK COMPLETE")
    print(final_output)
else:
    print(f"\n{'='*50}")
    print(f"WARNING: Max iterations ({max_iterations}) reached. Task may be incomplete.")
    print(f"Last controller output:\n{controllerSteps}")
```

---

## Loop Termination Conditions

| Condition | Action |
|-----------|--------|
| Controller output contains `[DONE]` | Exit loop, print final output |
| Controller output is empty or "no more steps" | Exit loop |
| `iteration_count >= max_iterations` | Force exit with warning |
| Tool caller calls no tools for 2 consecutive iterations | Exit loop |

---

## Sample CLI Usage

```bash
python main.py "create a calculator app" --max-iterations 50 --working-dir .
python main.py "build a web scraper" --max-iterations 100
python main.py "write tests for the calculator" --working-dir ./calculator
```

---

## What the Controller Sees Per Iteration

**Iteration 1 (initial):**
```
User: "create a function to add 2 numbers"
```
Output: `1) Use get_files_info to check existing files...`

**Iteration 2 (after tool results):**
```
Previous steps:
1) Use get_files_info to check existing files...
2) Create add.py with addition function...

Tool execution results:
Tool: get_files_info
Args: {"working_dir": ".", "current_dir": "."}
Result: -"add.py": file_size="0" is_dir="False" file_path=...

Tool: write_files_content
Args: {"working_dir": ".", "file_path": "add.py", "content": "def add(a, b):\n    return a + b\n"}
Result: Successfully wrote to file ...

Should you revise steps, continue, or mark done? If all write/run operations succeeded and no more steps needed, output [DONE].
```

**Iteration N (done):**
```
[DONE] Created add.py with an add function that takes two numbers and returns their sum.
```

---

## Variable Iteration Limit Strategy

Since the user wants this to be variable and adaptable:

| Use Case | Suggested `--max-iterations` |
|----------|------------------------------|
| Simple read-only queries | 5-10 |
| File creation / modifications | 20-30 |
| Complex multi-step projects | 50-100 |

**Recommendation:** Default to `50` but allow CLI override. The Controller's `[DONE]` signal will naturally stop the loop early for simple tasks.

---

## Implementation Order

1. **Update `prompts.py`** — Add `[DONE]` signal instructions and result-interpretation guidance to `controllerPrompt`
2. **Modify `functions/run_functions.py`** — Return structured dicts with `tool_call_id` instead of plain strings
3. **Add `format_tool_results` helper to `main.py`** — Format tool results for controller input
4. **Add CLI arguments to `main.py`** — `--max-iterations` and `--working-dir`
5. **Implement main while loop in `main.py`** — Controller → Tool Caller → Execute → Feed back to Controller
6. **Add final output handling** — `[DONE]` extraction and print summary
7. **Test with simple task** — e.g., "create a file called hello.py that prints hello world"

---

## Files Modified Summary

| File | Change Type |
|------|-------------|
| `prompts.py` | Modify — update controller and tool caller prompts |
| `main.py` | Modify — add CLI args, main loop, helper function |
| `functions/run_functions.py` | Modify — return structured results with tool_call_id |

---

## Open Questions / Items to Confirm

1. **Should `[DONE]` be a strict string match or a looser check** (e.g., controller just says "task complete" without the tag)?
2. **Should the tool caller also receive the iteration context**, or does only the Controller need to see full results?
3. **Should there be a `--verbose` flag** to print each iteration's steps and results to the console for transparency?
4. **Should the working directory be the current dir by default** (`.`) or should it be dynamically determined?
5. **Should the controller use the same model** (`llama-3.1-8b-instant`) for re-planning iterations, or a more capable model for later iterations?