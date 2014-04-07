# -*- coding: utf-8 -*-
__author__ = "Vladislav Ischenko"
# Python-curses Wargaming 02.04.2014 L3Problem


#### Function style ####


def load_code(filename):
    """
    Load code from file.
    filename: the name of file
    return: list - statement of forth code.
    """
    with open(filename, "r") as f:
        statement_list = []
        for line in f:
            statement_list.append(line.strip())
    return statement_list


def check_syntax(statement_list):
    """
    Check forth code syntax.
    statement_list: list
    # - comment
    each statement begin with new line
    should not be embedded quotes
    return: clean forth code.
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
    return: last statement result
    """
    stack = []
    compile_result = []

    def convert_to_number(num):
        """
        num: int, float, str
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

    # flow of execution
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
    lines: list
    return: file name
    """
    with open(filename, "w") as f:
        f.write('\n'.join(lines))
    return filename


#### Unit Tests for Fun ####


def UnitTestFun1():
    filename = 'forth1.txt'
    lines = [
        "put 1",
        "put 3",
        "add",
        "print",
    ]
    assert eval_forth(make_forth_file(filename, lines)) == 4


def UnitTestFun2():
    filename = 'forth2.txt'
    lines = [
        "put 4",
        "put 6",
        "add",
        "print",
    ]
    assert eval_forth(make_forth_file(filename, lines)) == 10


def UnitTestFun3():
    filename = 'forth3.txt'
    lines = [
        "put 1",
        "put 3",
        "sub",
        "print",
    ]
    assert eval_forth(make_forth_file(filename, lines)) == 2


#### Class style ####


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


class Parser(object):
    """
    Parsing code.
    """
    def __init__(self, statement_list):
        self.statement_list = statement_list
        self.clean_code = []

    def check_syntax(self):
        """
        statement_list: list
        Check forth code syntax
        # - comment
        each statement begin with new line
        should not be embedded quotes
        """
        for statement in self.statement_list:
            if '#' == statement[0][0]:
                continue
            s1 = "\'\'"
            s2 = "\"\""
            if s1 in statement or s2 in statement:
                raise ParserError('Error should not be embedded quotes')
            else:
                self.clean_code.append(statement)
        return self.clean_code


class Compiler(object):
    """
    Compiler for statement.
    """
    def __init__(self):
        self.stack = []
        self.compile_result = []

    def convert_to_number(self, num):
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

    def put(self, arg):
        self.stack.append(arg)
        return arg

    def pop(self):
        anws = self.stack.pop()
        return anws

    def add(self):
        anws1 = self.convert_to_number(self.pop())
        anws2 = self.convert_to_number(self.pop())
        try:
            anws = anws1 + anws2
        except TypeError:
            raise ParserError('Unsupported operand type(s)')
        self.put(anws)
        return anws

    def sub(self):
        anws1 = self.convert_to_number(self.pop())
        anws2 = self.convert_to_number(self.pop())
        anws = None
        if type(anws1) is str or type(anws2) is str:
            raise ParserError('Unsupported operand type(s)')
        else:
            anws = anws1 - anws2
            self.put(anws)
        return anws

    def fprint(self):
        anws = self.pop()
        print anws
        return anws


class Run(object):
    """
    Class for run forth code.
    """
    def __init__(self, filename, lines):
        self.filename = filename
        self.lines = lines
        self.statement_list = []
        self.result = []

    def make_forth_file(self):
        """
        Make file with forth's statements
        filename: name of file
        lines: list
        return: file name
        """
        with open(self.filename, "w") as f:
            f.write('\n'.join(self.lines))
        return self.filename

    def load_code(self):
        """
        Load code from file.
        filename: the name of file
        return: list - statement of forth code.
        """
        with open(self.filename, "r") as f:
            for line in f:
                self.statement_list.append(line.strip())
        return self.statement_list

    def eval_forth(self, clean_code, compiler):
        """
        Manager of flow of execution.
        clean_code: list
        compiler: Compiler obj.
        return last statement result.
        """
        for statement in clean_code:
            statement = statement.split()
            if statement[0] == 'put':
                self.result.append(compiler.put(statement[1]))
            elif statement[0] == 'pop':
                self.result.append(compiler.pop())
            elif statement[0] == 'add':
                self.result.append(compiler.add())
            elif statement[0] == 'sub':
                self.result.append(compiler.sub())
            elif statement[0] == 'print':
                self.result.append(compiler.fprint())

        return self.result[-1]


#
#
#### Unit Tests ####
#
#

class UnitTestClass():
    """
    For test class.
    """
    def __init__(self, filename, lines):
        self.filename = filename
        self.lines = lines

    def execute(self):
        # make file with forth code
        run = Run(self.filename, self.lines)
        run.make_forth_file()

        # load forth code
        run.load_code()

        pars = Parser(run.statement_list)

        # check syntax
        pars.check_syntax()

        # compile
        comp = Compiler()

        # eval_forth
        return run.eval_forth(pars.clean_code, comp)


# MAIN
# Run unit tests


if __name__ == '__main__':

    # Unit Test for Fun
    UnitTestFun1()
    UnitTestFun2()
    UnitTestFun3()

    # Test1
    filename1 = 'forth1_class.txt'
    lines1 = [
        "put 1",
        "put 3",
        "add",
        "print",
    ]

    # Test2
    filename2 = 'forth2_class.txt'
    lines2 = [
        "put 4",
        "put 6",
        "add",
        "print",
    ]

    filename3 = 'forth3_class.txt'
    lines3 = [
        "put 1",
        "put 3",
        "sub",
        "print",
    ]

    # Unit Test for Class
    test1 = UnitTestClass(filename1, lines1)
    assert test1.execute() == 4
    test2 = UnitTestClass(filename2, lines2)
    assert test2.execute() == 10
    test3 = UnitTestClass(filename3, lines3)
    assert test3.execute() == 2
