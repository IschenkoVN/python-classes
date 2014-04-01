# -*- coding: utf-8 -*-
# Python-curses Wargaming T2


def iter_lines(fd):
    """
    Read file lines.
    fd: filename
    """
    with open(fd, "r") as f:
        line = ""
        char = f.read(1)
        while char != "":
            if char == "\n":
                yield line
                line = ""
            else:
                line += char
            char = f.read(1)
        yield line


def strip_spaces(iter):
    """
    Remove spaces in lines.
    iter: iterator
    """
    for line in iter:
        yield line.strip()


def drop_empty(iter):
    """
    Delete empty lines.
    iter: iterator
    """
    for line in iter:
        if line != "":
            yield line


def split_items(iter):
    """
    Convert elements to python objects.
    iter: iterator
    """
    for line in iter:
        element_list = line.split()
        for element in element_list:
            if element.isdigit():
                # int
                yield int(element)
            else:
                try:
                    float(element)
                except ValueError, e:
                    # str
                    yield element
                else:
                    # float
                    yield float(element)


def get_ints(iter):
    """
    Objects with type int.
    iter: iterator
    """
    for element in iter:
        if type(element) == int:
            yield element


def my_sum(element_list):
    """
    Sum of objects with type int.
    element_list: sequence
    """
    return sum(element_list)


if __name__ == '__main__':

    fd = 'test.txt'
    line = "1 2 3 3.45 abra_cadabra    \n\n12"
    with open(fd, "w") as f:
        f.write(line)

    print list(iter_lines(fd))
    print list(strip_spaces(iter_lines(fd)))
    print list(drop_empty(strip_spaces(iter_lines(fd))))
    print list(split_items(drop_empty(strip_spaces(iter_lines(fd)))))
    print list(get_ints(split_items(drop_empty(strip_spaces(iter_lines(fd))))))
    print my_sum(get_ints(split_items(drop_empty(strip_spaces(iter_lines(fd))))))
