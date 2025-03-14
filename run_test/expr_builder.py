import math
import random

class ExprBuilder:
    def __init__(self):
        self.total_ops = 0 # Number of operators in last generated expression
        self.num_ops = {} # Number of ops in expression
        self.valid = ( # Holds possible functions and operators
            # (clCalc format, Python format, weight for random choice, display icon)
            ('? + $', '? + $', 10, '+'),
            ('? - $', '? - $', 10, '-'),
            ('? * $', '? * $', 5, '*'),
            ('? / $', '? / $', 5, '/'),
            ('?^$', '?**$', 3, '^'),
            ('sqrt(?)', 'math.sqrt(?)', 3, '√'),
            ('log(?)', 'math.log10(?)', 2, 'log_10'),
            ('ln(?)', 'math.log(?)', 2, 'ln'),
            ('sin(?)', 'math.sin(?)', 1, 'sin'),
            ('cos(?)', 'math.cos(?)', 1, 'cos'),
            ('tan(?)', 'math.tan(?)', 1, 'tan'),
            ('cot(?)', '(1 / math.tan(?))', 0.7, 'cot'),
            ('? / 0', '? / 0', 0.5, '/') # Introduce divide by zero errors
        )

    # Wrapper function to generate expressions
    def get_expr(self):
        self.total_ops = 0
        self.num_ops = {}
        clc, py = self.get_sub_expr(False, False)
        return clc, py

    # Recursively generates expressions
    def get_sub_expr(self, exp, non_neg):
        if random.random() <= self.end_prob() and self.total_ops > 1:
            num = self.get_num(exp, non_neg)
            return num, num

        # Select next operator
        clc_next, py_next = self.select_func()
        self.total_ops += 1

        # Check if negatives should be prevented
        neg = self.check_neg(clc_next)
        if non_neg is True:
            neg = True # Prevent Negatives

        # Check if exponent
        if exp or '^' in clc_next:
            new_exp = True
        else:
            new_exp = False

        # Generate sub -expressions in random order
        if random.random() <= 0.5:
            clc_next, py_next = self.replace_exp('?', clc_next, py_next, exp, neg)
            clc_next, py_next = self.replace_exp('$', clc_next, py_next, new_exp, neg)
        else:
            clc_next, py_next = self.replace_exp('$', clc_next, py_next, new_exp, neg)
            clc_next, py_next = self.replace_exp('?', clc_next, py_next, exp, neg)


        if random.random() <= 0.3: # Add Parentheses
            clc_next = f'({clc_next})'
            py_next = f'({py_next})'

        if random.random() <= 0.025: # Randomly add errors
            clc_next, py_next = self.get_syntax_err(clc_next, py_next)
        return clc_next, py_next

    # Replace icon character with generated sub-expression
    def replace_exp(self, icon, clc_next, py_next, exp, neg):
        if icon in clc_next: #  Replace icon with sub-expression
            clc, py = self.get_sub_expr(exp, neg)
            return clc_next.replace(icon, clc), py_next.replace(icon, py)
        return clc_next, py_next

    def select_func(self):
        weights = [item[-2] for item in self.valid]
        next_expr = random.choices(self.valid, weights=weights, k=1)
        self.update_ops(next_expr[0][-1])
        return next_expr[0][0], next_expr[0][1]

    def update_ops(self, op):
        if op in self.num_ops:
            self.num_ops[op] += 1
        else:
            self.num_ops[op] = 1

    def get_syntax_err(self, clc, py):
        errors = ('Wxd', 'INVALID', '@', '#', 'THIS_IS_A_SYNTAX_ERROR')
        err = random.choice(errors)
        clc = f'{err}{clc}'
        py = f'{err}{py}'
        return clc, py

    # Prevent negatives operands inside square roots and logarithms
    # Complex numbers can still be produced through subtraction in sub-expressions and non-integer exponents
    def check_neg(self, expr):
        if 'sqrt' in expr or 'l' in expr:
            return True

        return False

    # Probability of ending
    def end_prob(self):
        return 1.5 * (1 - math.e ** (-0.1 * self.total_ops)) ** 3

    # Randomly generates next number
    def get_num(self, exp, neg):
        num_range = 1000
        if exp: # Smaller numbers when exponent to reduce range errors
            num_range = 5

        num = random.randint(0, num_range)
        if random.random() <= 0.5:  # Return decimal 50% of the time
            dec_places = random.randint(1, 5)
            num += round(random.random(), dec_places)
        if not neg and random.random() <= 0.15:
            num *= -1 # Return negative 15% of time
        return str(num)

