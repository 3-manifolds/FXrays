import doctest
import sys
from . import _test

def runtests():
    return doctest.testmod(_test)

if __name__ == '__main__':
    failures, tests = runtests()
    sys.exit(failures)
