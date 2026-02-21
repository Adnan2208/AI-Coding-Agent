from functions.get_files_content import get_files_content

def main():

    # Fix both logic in get_files_info()
    print(get_files_content("calculator","main.py"))
    print(get_files_content("calculator","pkg/calculator.py"))
    print(get_files_content("calculator","bin"))
    print(get_files_content("calculator","pkg/does_not_exist.py"))

main()