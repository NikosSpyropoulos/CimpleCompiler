# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

table = {}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class RecordScope:
    def __init__(self, entities, nestingLevel):
        self.entities = entities
        self.nestingLevel = nestingLevel


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    symbols_table = []
    symbols_table.append([])
    symbols_table.append([])
    symbols_table.append([])
    symbols_table[0].append(['a', 'p'])
    symbols_table[1].append(['a', 'b'])
    symbols_table[2].append(['o', 'k'])
    a = []
    a = [1,2]

    for item in a:

        print(item)
    level = 0

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
