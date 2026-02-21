from functions.write_files_content import write_files_content

def main():

    print(write_files_content("calculator","asdf.py","print(hello world)"))
    print(write_files_content("calculator","../hello","should not type"))

main()