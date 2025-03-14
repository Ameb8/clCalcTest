import math
from logging import exception


def test_expr(expr):
    try:
        res = eval(expr)
    except Exception as e:
        res = None

    return res

print(test_expr('log10(0)'))
print(test_expr('sqrt(-1)'))
print(test_expr('4 / 0'))
print(test_expr('1000000000**1000000000000000000'))
