import math
import random

class ExprBuilder:
    def __init__(self):
        self.num_ops = 0 # Number of operators in last generated expression
        self.valid = ( # Holds possible functions and operators
            # (clCalc format, Python format, weight for random choice, display icon)
            ('? + $', '? + $', 10, '+'),
            ('? - $', '? - $', 10, '-'),
            ('? * $', '? * $', 5, '*'),
            ('?^$', '?**$', 3, '^'),
            ('sqrt(?)', 'math.sqrt(?)', 3, '√'),
            ('log(?)', 'math.log10(?)', 2, 'log_10'),
            ('ln(?)', 'math.log(?)', 2, 'ln'),
            ('sin(?)', 'math.sin(?)', 1, 'sin'),
            ('cos(?)', 'math.cos(?)', 1, 'cos'),
            ('tan(?)', 'math.tan(?)', 1, 'tan'),
            ('cot(?)', '(1 / math.tan(?))', 0.7, 'cot')
        )

    # Wrapper function to generate expressions
    def get_expr(self):
        self.num_ops = 0
        clc, py = self.get_sub_expr()
        return clc, py

    # Recursively generates expressions
    def get_sub_expr(self):
        if random.random() <= self.end_prob() and self.num_ops > 1:
            num = self.get_num()
            return num, num

        # Select next operator
        clc_next, py_next = self.select_func()
        self.num_ops += 1

        # Generate sub -expressions in random order
        if random.random() <= 0.5:
            clc_next, py_next = self.replace_exp('?', clc_next, py_next)
            clc_next, py_next = self.replace_exp('$', clc_next, py_next)
        else:
            clc_next, py_next = self.replace_exp('$', clc_next, py_next)
            clc_next, py_next = self.replace_exp('?', clc_next, py_next)


        if random.random() <= 0.3: # Add Parentheses
            clc_next = f'({clc_next})'
            py_next = f'({py_next})'

        return clc_next, py_next

    # Replace icon character with generated sub-expression
    def replace_exp(self, icon, clc_next, py_next):
        if icon in clc_next: #  Replace icon with sub-expression
            clc, py = self.get_sub_expr()
            return clc_next.replace(icon, clc), py_next.replace(icon, py)
        return clc_next, py_next

    def select_func(self):
        weights = [item[-2] for item in self.valid]
        next_expr = random.choices(self.valid, weights=weights, k=1)
        return next_expr[0][0], next_expr[0][1]

    # Probability of ending
    def end_prob(self):
        return (1 - math.e ** (-0.1 * self.num_ops)) ** 3

    # Randomly generates next number
    def get_num(self):
        num = 0
        if random.random() <= 0.5:  # Return decimal 50% of the time
            num = random.randint(-50, 50)
        else:
            num = random.randrange(0, 50)
        if random.random() <= 0.15:
            num *= -1 # Return negative 15% of time
        return str(num)

builder = ExprBuilder()
for i in range(5):
    expr, py_expr = builder.get_expr()
    print(f'expression {i} ({builder.num_ops}): {expr} = {eval(str(py_expr))}')