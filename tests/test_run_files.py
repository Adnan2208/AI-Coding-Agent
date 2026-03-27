import sys
sys.path.append("/home/adnan/Adnan/Ai-agent/")

from functions import run_files

def main():

    print(run_files("calculator","main.py"))
    print(run_files("calculator","test.py"))

main()
