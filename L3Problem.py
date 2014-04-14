# -*- coding: utf-8 -*-
__author__ = "Vladislav Ischenko"
# Python-curses Wargaming 02.04.2014 L3Problem


class Error(Exception):
    """
    Base class for exceptions.
    """
    pass


class ParserError(Error):
    """
    Exception raised for errors.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


#### Function style ####


def convert_to_number(num):
    """
    num: int, float, str
    Convert num to number, else return num (str).
    """
    try:
        return int(num)
    except ValueError:
        try:
            return float(num)
        except ValueError:
            return num


def parse(code_line_list):
    """
    Check forth code syntax.
    code_line_list: list of lines of forth's code.
    return: None or yield statement.
    """
    VALID_STATEMENTS = [
        "put",
        "pop",
        "add",
        "sub",
        "print",
    ]

    for line in code_line_list:
        if line[0].startswith("#"):
            continue
        # We have two or one parameters,
        # that's why we work only with first and second element.

        items = line.split()
        if items[0] in VALID_STATEMENTS:
            if len(items) > 1:
                yield [items[0], convert_to_number(items[1])]
            elif len(items) == 1:
                yield [items[0]]
        else:
            raise ParserError('ERROR: Syntax error')


@provides("put", 1, 0)
def put(stack, arg):
    stack.append(arg)
    return arg


def pop(stack):
    result = stack.pop()
    return result


def add(stack):
    result1 = pop(stack)
    result2 = pop(stack)
    try:
        result = result1 + result2
    except TypeError:
        raise ParserError('ERROR: Unsupported operand type(s)')
    put(stack, result)
    return result

@privides("sub", 0, 2)
def sub(stack):
    put(stack, pop(stack) - pop(stack))

@provides("print", 0, 1)
def fprint(stack):
    result = pop(stack)
    print result
    return result

all_commands = {}
def provides(cmd_name):


def eval_forth(code_statements):
    """
    Run forth code.
    code_statements: list of lines of forth's code.
    """
    stack = []
    eval_result = []

    try:
    for statement in parse(code_statements):
        if statement[0] == 'put':
            eval_result.append(put(stack, statement[1]))
        elif statement[0] == 'pop':
            eval_result.append(pop(stack))
        elif statement[0] == 'add':
            eval_result.append(add(stack))
        elif statement[0] == 'sub':
            eval_result.append(sub(stack))
        elif statement[0] == 'print':
            eval_result.append(fprint(stack))

    return eval_result[-1]


#### Unit Tests for Fun ####


def unit_test_fun(filename, lines, answer):
    """
    data: dict
    Exemple od data object:
        {filename: [lines, answer], }
    """

    # Make file with forth's statements
    with open(filename, "w") as f:
        f.write('\n'.join(lines))

    # Load code
    with open(filename) as f:
        code_line_list = [i.strip() for i in f]

    assert eval_forth(code_line_list) == answer


#### Class style ####

# Переписать класс Command
# избавится от ифов


class Run(object):

    def __init__(self, parser, compiler):
        self.parser = parser
        self.compiler = compiler

    def eval_forth(self):
        """
        Run forth code.
        code_statements: list of lines of forth's code.
        """

        for statement in self.parser.parse():
            if statement[0] == 'put':
                self.compiler.compile_result.append(self.compiler.put(statement[1]))
            elif statement[0] == 'pop':
                self.compiler.compile_result.append(self.compiler.pop())
            elif statement[0] == 'add':
                self.compiler.compile_result.append(self.compiler.add())
            elif statement[0] == 'sub':
                self.compiler.compile_result.append(self.compiler.sub())
            elif statement[0] == 'print':
                self.compiler.compile_result.append(self.compiler.fprint())

        return self.compiler.compile_result[-1]


#### Unit Tests ####


if __name__ == '__main__':

    # Data
    filename1 = 'forth1.txt'
    lines1 = (4, [
        "put 1",
        "put 3",
        "add",
        "print",
    ])

    filename2 = 'forth2.txt'
    lines2 = [
        "put 4",
        "put 6",
        "add",
        "print",
    ]
    answer2 = 10

    filename3 = 'forth3.txt'
    lines3 = [
        "put 1",
        "put 3",
        "sub",
        "print",
    ]
    answer3 = 2

    data = [
        (filename1, lines1, answer1),
        (filename2, lines2, answer2),
        (filename3, lines3, answer3),
    ]

    # Run unit tests for functions style.
    for item in data:
        unit_test_fun(*item)
