import functools


def twoargs(one, two):
    print(one, two)


f = functools.partial(twoargs, "1")

f(2)
