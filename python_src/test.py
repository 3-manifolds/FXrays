import doctest
from . import _test

def runtests():
    return doctest.testmod(_test)

if __name__ == '__main__':
    runtests()
