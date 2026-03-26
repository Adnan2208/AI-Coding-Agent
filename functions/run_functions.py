import json
from availableFunctions import availableFunctions

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
        results.append(res)

    return results
