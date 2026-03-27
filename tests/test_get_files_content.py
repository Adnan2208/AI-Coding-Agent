import sys
sys.path.append("/home/adnan/Adnan/Ai-agent/")

from functions import get_files_content

def main():

    print(get_files_content("calculator","main.py"))
    print(get_files_content("calculator","pkg/calculator.py"))
    print(get_files_content("calculator","bin"))
    print(get_files_content("calculator","pkg/does_not_exist.py"))

main()