# -*- coding: utf-8 -*-
__author__ = "Vladislav Ischenko"
# Python-curses Wargaming 02.04.2014 L3Problem


#### Function style ####


def load_code(filename):
    """
    Load code from file.
    filename: the name of file
    return: str - forth code
    """
    with open(filename, "r") as f:
        statement_list = []
        for line in f:
            statement_list.append(line.strip())
    return statement_list


def check_syntax(statement_list):
    """
    statement_list: list
    Check forth code syntax
    # - comment
    each statement begin with new line
    should not be embedded quotes
    """
    clean_code = []
    for statement in statement_list:
        if '#' == statement[0][0]:
            continue
        s1 = "\'\'"
        s2 = "\"\""
        if s1 in statement or s2 in statement:
            print 'Error should not be embedded quotes'
            break
        else:
            clean_code.append(statement)
    return clean_code


def compile(clean_code):
    """
    clean_code: list
    Statements:
        put
        pop
        add
        sub
        print
    return: last compile_result
    """
    stack = []
    compile_result = []

    def convert_to_number(num):
        """
        Convert num to number, else return num (str).
        """
        if num.isdigit():
            return int(num)
        else:
            try:
                return float(num)
            except ValueError:
                return num

    def put(arg):
        stack.append(arg)
        return arg

    def pop():
        p = stack.pop()
        return p

    def add():
        p1 = convert_to_number(pop())
        p2 = convert_to_number(pop())
        p3 = p1 + p2
        put(p3)
        return p3

    def sub():
        p1 = convert_to_number(pop())
        p2 = convert_to_number(pop())
        p3 = None
        if type(p1) is not str or type(p2) is not str:
            p3 = p1 - p2
            put(p3)
        return p3

    def fprint():
        p = pop()
        print p
        return p

    for statement in clean_code:
        statement = statement.split()
        if statement[0] == 'put':
            compile_result.append(put(statement[1]))
        elif statement[0] == 'pop':
            compile_result.append(pop())
        elif statement[0] == 'add':
            compile_result.append(add())
        elif statement[0] == 'sub':
            compile_result.append(sub())
        elif statement[0] == 'print':
            compile_result.append(fprint())

    return compile_result[-1]


def eval_forth(filename):
    """
    Run forth code.
    filename: name of file with forth code.
    """
    forth_code = load_code(filename)
    clean_code = check_syntax(forth_code)
    return compile(clean_code)


def make_forth_file(filename, lines):
    """
    Make file with forth's statements
    filename: name of file
    lines: str
    return: filename
    """
    with open(filename, "w") as f:
        f.write('\n'.join(lines))
    return filename


#### Unit Tests ####


def UnitTest1():
    filename = 'forth1.txt'
    lines = [
        "put 1",
        "put 3",
        "add",
        "print",
    ]
    assert eval_forth(make_forth_file(filename, lines)) == 4


def UnitTest2():
    filename = 'forth2.txt'
    lines = [
        "put 4",
        "put 6",
        "add",
        "print",
    ]
    assert eval_forth(make_forth_file(filename, lines)) == 10


#### Class style ####


if __name__ == '__main__':
    UnitTest1()
    UnitTest2()
