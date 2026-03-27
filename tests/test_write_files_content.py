import sys
sys.path.append("/home/adnan/Adnan/Ai-agent/")

from functions import write_files_content

def main():

    print(write_files_content("calculator","asdf.py","print(hello world)"))
    print(write_files_content("calculator","../hello","should not type")) #This should not work

main()