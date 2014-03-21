# -*- coding: utf-8 -*-

# Python-curses Wargaming 03.2014
# Task 1)


def bigest(x, y):
    """
    x, y : int
    return bigest number
    if equal return y
    """
    if x > y:
        return x
    return y


def smaler(x, y):
    """
    x, y : int
    return smaler number
    if equal return x
    """
    if x < y:
        return x
    return y


def midle(a, b, c):
    """
    Base fun for finde midle nimber.
    a, b, c: int
    return int
    """
    x = bigest(a, b)
    y = bigest(c, a)
    if x == y:
        x = smaler(a, b)
        y = smaler(c, a)
        return bigest(x, y)
    return smaler(x, y)


def midleIf(a, b, c):
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
        return bigest(b, c)
    if b == maxi:
        return bigest(a, c)
    if c == maxi:
        return bigest(a, b)


# Task 2) page 6


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


if __name__ == '__main__':

    # test midle def
    test(midle)

    # test midleIf
    test(midleIf)
