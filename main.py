# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
keywords = ["program", "declare", "function", "procedure", "in", "inout", "if", "else", "while", "switchcase",
            "case", "default", "forcase", "incase", "return", "call", "print", "input", "or", "and", "not"]

char = "program"
if char in keywords:
    print(char + "_tk")

keyword_dict = {
    "program": "program_tk",
    "declare": "declare_tk",
    "function": "function_tk",
    "procedure": "procedure_tk",
    "in": "in_tk",
    "inout": "inout_tk",
    "if": "if_tk",
    "else": "else_tk",
    "while": "while_tk",
    "switchcase": "switchcase_tk",
    "case": "case_tk",
    "default": "default_tk",
    "forcase": "forcase_tk",
    "incase": "incase_tk",
    "return": "return_tk"
}
if char == "program_tk":
    print("yes")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
