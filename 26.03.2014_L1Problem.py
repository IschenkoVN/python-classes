# -*- coding: utf-8 -*-

# Python-curses Wargaming 03.2014
# Task 1)


def get_biggest(x, y):
    """
    x, y : int
    return biggest number
    if equal return y
    """
    return x if x > y else y



def get_smaller(x, y):
    """
    x, y : int
    return smaller number
    if equal return x
    """
    return x + y - get_biggest(x, y)


def get_middle(a, b, c):
    """
    Base fun for finde midle nimber.
    a, b, c: int
    return int
    """
    x = get_biggest(a, b)
    y = get_biggest(c, a)
    if x == y:
        x = get_smaller(a, b)
        y = get_smaller(c, a)
        return get_biggest(x, y)
    return get_smaller(x, y)


def get_middle2(a, b, c):
    max_v = get_biggest(get_biggest(a, b), c)
    min_v = get_smaller(get_smaller(a, b), c)
    return a + b + c - min_v - max_v


def middle_if_only(a, b, c):
    """
    Use omly IF statments.
    """
    # find max
    if a >= b:
        if a > c:
            maxi = a
        else:
            maxi = c
    if b >= a:
        if b > c:
            maxi = b
        else:
            maxi = c

    # ignore maxi element
    if a == maxi:
        return get_biggest(b, c)
    if b == maxi:
        return get_biggest(a, c)
    if c == maxi:
        return get_biggest(a, b)


def midleSorted(a, b, c):
    """
    Fun for cheking.
    """
    return sorted([a, b, c])[1]


def test(fun):
    """
    Test fun and test data
    fun: def
    def: a, b, c: int
    """
    L1 = (1, 2, 3)
    L2 = (1, 3, 2)
    L3 = (2, 3, 1)
    L4 = (3, 2, 1)
    L5 = (1, 1, 1)
    L6 = (2, 1, 3)
    L7 = (2, 2, 3)
    L8 = (2, 2, 1)
    for el in (L1, L2, L3, L4, L5, L6, L7, L8):
        assert fun(*el) == midleSorted(*el)


# Task 2) AOH

def decode_AON(data):
    char_list = list(data)
    result_list = []
    proxy_list = []
    for index, elem in enumerate(char_list):
        next_index = index + 1
        pre_index = index - 1
        if next_index < len(char_list):
            if elem == char_list[next_index]:
                if elem == '#':
                    if len(result_list) > 0:
                        proxy_list.append(result_list[-1])
                else:
                    proxy_list.append(elem)
            else:
                if proxy_list:
                    result_list.append(proxy_list[0])
                    proxy_list = []
    else:
        if proxy_list:
            result_list.append(proxy_list[0])

    return ''.join(result_list)


def testTas2(fun):
    assert fun("") == ""
    assert fun("1") == ""
    assert fun("11") == "1"
    assert fun("11111") == "1"
    assert fun("11#") == "1"
    assert fun("11##") == "11"
    assert fun("11122234###55") == "1225"
    assert fun("4434###311333661") == "44136"
    assert fun("##11122234###55") == "1225"
    assert fun("11##11##") == "1111"


if __name__ == '__main__':

    # Task 1)

    # test get_middle
    test(get_middle)

    # test get_middle2
    test(get_middle2)

    # test get_middle2
    test(get_middle2)

    # Task 2)
    testTas2(decode_AON)
