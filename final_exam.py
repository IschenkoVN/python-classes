# -*- coding: utf-8 -*-
__author__ = "Vladislav Ischenko"
# Python-curses Wargaming Final exam.

import re


"""Print Table

Печать таблицы. Задана таблица в виде словаря, где строка заголовка
отображается в массив значений-колонок. Длины всех массивов-значений
одиноковые, нужно напечатать ее в следующем виде:

+---------+---------+---------+---------+
| Header1 | Header2 | Header3 | Header4 |
+---------+---------+---------+---------+
|  val1   |  ....   |         |         |
|  val2   |         |         |         |
| vvaaal3 |         |         |         |
|  ....   |         |         |         |
+---------+---------+---------+---------+

Для ширины колонки должна выбираться максимальная длинна помещаемого
в нее текста + 2. Текст должен центрироваться пробелами внутри ячейки.

input: dict, key: str, value: list.
{"header1": ['val1', 'val2', 'val3'], "header2": ['val1', 'val2', 'val3']}
The len's of all lists is equal.
"""


def print_table(data):
    """
    data: dict, key: str, value: list.
    return: str
    """
    if not data:
        return ''
    # Find element with max len in data.
    # в задании не говориться, что значения - только строки
    # каждая колонка должна именть свою ширину
    # эта строка совершенно не читаема, например нельзя просто взглянув на нее понять
    # какой функции накоторый параметр
    column_width = len(max(max([max(
        elem_list, key=len) for elem_list in data.itervalues()], key=len), max(
            data.keys(), key=len), key=len))
            
    # First and last row of table.
    separator = '+' + '+'.join(
        ['-' * (column_width + 2) for key in data.keys()]) + '+'
    # Header of table.
    row_list = [
        separator,
        '| ' + ' | '.join(
            [key.center(column_width) for key in data.keys()]) + ' |',
        separator
    ]
    # Rows of table.
    for value_couples in zip(*data.values()):
        row_list.append('| '+' | '.join(
            [str(elem).center(column_width) for elem in value_couples])+' |')
    row_list.append(separator)
    return '\n'.join(row_list)


"""Arithmetic expression

Посчитать арифметическое выражение.
Строка состоить из чисел и знаков '+', '-', '*' и пробелов.
Определить является ли строка корректным математическим выражением и посчитать
 его значение.
Корректным считается выражение, которое начинается с числа,
оканчивается числом и в котором не встречаются подрят два числа или два знака.
Пробелы могут находиться где угодно.
При расчете выражения учитывать приоритет операторов.

"1 2+3","1 2+-3"  - не корректные выражения
"1 + 2-3* 77" - корректное выражение

input: str,
operators: '+', '-', '*'

Solutions:
The Algorithm "Top-Down Parsing"

"""

# способ передачи состояния через глобальную переменную 
# как раз пример того, где глобальные переменные применяться не должны никогда


token_pat = re.compile("\s*(?:(\d*\.\d+|\d+)|(.))")


def to_number(number):
    try:
        return int(number)
    except ValueError:
        try:
            return float(number)
        except ValueError:
            raise SyntaxError(u"Syntax Error")


class LiteralToken(object):
    def __init__(self, value):
        self.value = value

    def nud(self):
        return self.value


class OperatorAddToken(object):
    lbp = 10

    def led(self, left):
        right = expression(10)
        return left + right


class OperatorSubToken(object):
    lbp = 10

    def led(self, left):
        return left - expression(10)


class OperatorMulToken(object):
    lbp = 20

    def led(self, left):
        return left * expression(20)


class EndToken(object):
    lbp = 0


def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    try:
        while rbp < token.lbp:
            t = token
            token = next()
            left = t.led(left)
    except AttributeError:
        raise SyntaxError(u"Syntax Error")
    return left


def tokenize(program):
    for number, operator in token_pat.findall(program):
        if number:
            yield LiteralToken(to_number(number))
        elif operator == "+":
            yield OperatorAddToken()
        elif operator == "-":
            yield OperatorSubToken()
        elif operator == "*":
            yield OperatorMulToken()
        else:
            raise SyntaxError(u"Syntax Error")
    yield EndToken()


def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()


"""Rendering variables to templates
Напишите класс для подстановки переменных в тексте. На вход подается текст,
с конструкциями вида {{ var_name }}, где var_name является корректным
именем python переменной. Их необходимо заменить на
значения именованных параметров, переданных в метод форматирования шаблона.

# filename content
# X={{x}} y={{y}}
#

t = Template(filename)
print t.fill(x='12', y=13)      # prints "X=12 y=13"
"""

from string import Template


class TemplateInit(Template):
    idpattern = '[a-z]+_[a-z]+'
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''

    def __init__(self, filename):
        with open(filename) as f:
            lines = [i.strip() for i in f]
        super(TemplateInit, self).__init__('\n'.join(lines))


if __name__ == '__main__':

    # Print Table
    data = {
        "O": ['12345', '12346', '1234567', '12'],
        "h0": ['val1', 'val12', 'val123', 'val1234'],
        "h2": ['12345', '12346', '1234567', '12345678'],
        "h3": ['12345', '12346', '1234567', '12345678'],
    }
    print print_table(data)
    # Just for fun =) One row.
    res = '\n'.join(['+' + '+'.join(['-' * (len(max(max([max(elem_list, key=len) for elem_list in data.itervalues()], key=len), max(data.keys(), key=len), key=len)) + 2) for key in data.keys()]) + '+'] + ['| ' + ' | '.join([key.center(len(max(max([max(elem_list, key=len) for elem_list in data.itervalues()], key=len), max(data.keys(), key=len), key=len))) for key in data.keys()]) + ' |'] + ['+' + '+'.join(['-' * (len(max(max([max(elem_list, key=len) for elem_list in data.itervalues()], key=len), max(data.keys(), key=len), key=len)) + 2) for key in data.keys()]) + '+'] +['| '+' | '.join([str(elem).center(len(max(max([max(elem_list, key=len) for elem_list in data.itervalues()], key=len), max(data.keys(), key=len), key=len))) for elem in value_couples])+' |' for value_couples in zip(*data.values())] + ['+' + '+'.join(['-' * (len(max(max([max(elem_list, key=len) for elem_list in data.itervalues()], key=len), max(data.keys(), key=len), key=len)) + 2) for key in data.keys()]) + '+'])
    assert print_table(data) == res

    # Arithmetic expression "Top-Down Parsing"
    assert parse("1 +    2 +  7") == 1 +    2 +  7
    assert parse("1 + 1.5 * 4 + 3") == 1 + 1.5 * 4 + 3
    assert parse("1 + 1.5+1.5* 96") == 1 + 1.5+1.5* 96

    # Rendering variables to templates
    filename = 'templates.txt'
    with open(filename, "w") as f:
        f.write('X={{x}} y={{y}}')

    ti = TemplateInit(filename)
    assert ti.safe_substitute(x='12', y=13) == "X=12 y=13"
