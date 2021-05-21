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
    score = RecordScope({1, 2, 3}, 5)
    score1 = RecordScope({18, 28, 38}, 85)
    score2= RecordScope({3,5,6}, 8)

    table = []
    table.append(score)
    table.append(score1)
    table.append(score2)
    table.remove(score1)
    for index,sco in enumerate(table):

        print(sco.entities ,'a')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
