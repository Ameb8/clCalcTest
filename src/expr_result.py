import math
from operator import truediv


class ExprResult:
    def __init__(self):
        self.result = None
        self.math_err = False
        self.syntax_err = False

    '''
    # Compare all fields for equality
    def __eq__(self, other):
        if not isinstance(other, self.__class__): #Compare object types
            return False

        # Check expression results
        if not self.result is None and not other.result is None:
            # Check approximately if results calculated
            if round(self.result, 2) == round(other.result, 2):
                return False
        elif self.result != other.result:
            return False

        return ( # Compare detected errors
            self.math_err == other.math_err,
            self.syntax_err == other.syntax_err
        )
    '''

    def __eq__(self, other):
        if not self.result is None and not other.result is None: # Both calculated result
            if abs(self.result - other.result) < 0.001:
                return True
        if self.math_err is True and other.math_err is True:
            return True
        if self.syntax_err is True and other.syntax_err is True:
            return True

        return False

    '''
    def __str__(self):
        obj_str = []
        if self.result is None:
            obj_str.append('Expression could not be evaluated')
        else:
            obj_str.append(f'\nExpression Result: {self.result}')

        if self.math_err:
            obj_str.append('\nMathematical Error Detected')
        if self.syntax_err:
            obj_str.append('\nSyntax Error Detected')

        return "\n".join(obj_str)
