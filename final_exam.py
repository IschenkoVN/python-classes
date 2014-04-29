# -*- coding: utf-8 -*-
__author__ = "Vladislav Ischenko"
# Python-curses Wargaming Final exam.


"""Print Table.
input: dict, key: str, value: list.
{"header1": ['val1', 'val2', 'val3'], "header2": ['val1', 'val2', 'val3']}
The len's of all lists is equal.
"""


def print_table(data):
    """
    data: dict, key: str, value: list.
    """
    # Find element with max len in data.
    column_width = len(max(max([max(elem_list, key=len) for elem_list in data.itervalues()], key=len),
        max(data.keys(), key=len), key=len))

    separator = '+' + '+'.join(
        ['-' * (column_width + 2) for key in data.keys()]) + '+'

    # Print header of table.
    row_list = [separator]
    row_list.append('| ' + ' | '.join([key.center(column_width) for key in data.keys()]) + ' |')
    row_list.append(separator)

    # Print table rows
    for value_couples in zip(*data.values()):
        row_list.append('| '+' | '.join([str(elem).center(column_width) for elem in value_couples])+' |')

    row_list.append(separator)

    return '\n'.join(row_list)


"""
Обратная польская запись.
http://habrahabr.ru/post/100869/
"""

if __name__ == '__main__':
    data = {
        "O": ['12345', '12346', '1234567', '12'],
        "h0": ['val1', 'val12', 'val123', 'val1234'],
        "h2": ['12345', '12346', '1234567', '12345678'],
        "h3": ['12345', '12346', '1234567', '12345678'],
    }
    print print_table(data)
