import sys
sys.path.append("/home/adnan/Adnan/Ai-agent/")

from functions import get_files_info

def main():

    print(get_files_info("calculator","."))
    print(get_files_info("calculator","pkg"))
    print(get_files_info("calculator","../"))
    print(get_files_info("calculator","bin"))
    print(get_files_info("calculator"))

main()