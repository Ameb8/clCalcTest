class ExprResult:
    def __init__(self):
        self.result = None
        self.math_err = False
        self.syntax_err = False

    def __eq__(self, other):
        if not self.result is None and not other.result is None: # Both calculated result
            if abs(self.result - other.result) <= 0.01:
                return True
        if self.syntax_err is True and other.syntax_err is True:
            return True
        if self.math_err is True and other.math_err is True:
            return True
        return False

    def __str__(self):
        str = []
        if self.result is None:
            str.append('Expression could not be evaluated')
        else:
            str.append(f'Expression evaluates to: {self.result}')
        if self.math_err or self.syntax_err:
            if self.math_err:
                str.append(', Math Error Detected')
            if self.syntax_err:
                str.append(', Syntax Error Detected')
        return ''.join(str)


def get_result(expr):
    expr_result = ExprResult()
    try:
        expr_result.result = eval(expr)
    except (ValueError, ZeroDivisionError):
        expr_result.math_err = True
    except OverflowError:
        return None
    except Exception:
        expr_result.syntax_err = True
    return expr_result
