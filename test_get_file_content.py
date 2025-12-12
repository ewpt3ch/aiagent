from functions.get_file_content import get_file_content

print(get_file_content("calculator", "lorem.txt")[10000:])
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/not_exist.py"))

