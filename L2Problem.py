# -*- coding: utf-8 -*-
# Python-curses Wargaming T2


def iter_lines(fname): # fd stands for File Descriptor
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
        for element in line.split():
            if element.isdigit():
                # int
                yield int(element)
            else:
                try:
                    yield float(element)
                except ValueError:
                # except ValueError as e:
                # never use (except ValueError, e) - this may cause a tricky error
                    # str
                    yield element


def get_ints(iter):
    """
    Objects with type int.
    iter: iterator
    """
    for element in iter:
        if type(element) is int: # use is instead of == to compare with singleton
            yield element


def my_sum(element_list):
    """
    Sum of objects with type int.
    element_list: sequence
    """
    return sum(element_list)


#
# THERE SHOULD BE A UNIT-TESTS!
#

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
