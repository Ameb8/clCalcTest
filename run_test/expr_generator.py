import random
import math


class HiddenMarkov:
    def __init__(self, len_scale=1.0):
        self.len_scale = len_scale
        self.length = 0
        self.close_pars_needed = 0

        self.end = ('END', self.end_prob)
        self.close_par = ('PAR_CLOSE', self.close_par_prob)

        self.ops_in_expr = set() # Holds operators and functions used in expression

        self.next_term_probs = {
            "START": [('INVALID', lambda: 0.001), ('NUM', lambda: 0.5), ('PAR_OPEN', lambda: 0.5), ('FUNC', lambda: 1)],
            "NUM": [('INVALID', lambda: 0.001), self.end, self.close_par, ("OP", lambda: 0.7)],
            "OP": [('INVALID', lambda: 0.001), ('FUNC', lambda: 0.25), ('PAR_OPEN', lambda: 0.25), ('NUM', lambda: 1)],
            'PAR_OPEN': [('INVALID', lambda: 0.001), ('NUM', lambda: 0.5), ('PAR_OPEN', lambda: 0.25), ('FUNC', lambda: 1)],
            'PAR_CLOSE': [('INVALID', lambda: 0.001), self.end, self.close_par, ('OP', lambda: 1)],
            'FUNC': [('INVALID', lambda: 0.001), self.end, self.close_par, ('OP', lambda: 1)],
            'INVALID': [self.end, self.close_par, ('OP', lambda: 0.5), ('NUM', lambda: 1)]
        }

    def generate_expr(self, len_scale=0.5):
        state = "START"
        clc_expr = []
        py_expr = []
        self.length = 0
        state = 'START'

        funcs = ('sqrt', 'ln', 'cos', 'sin', 'tan', 'cot')
        invalid = ('@', 'sdfsv', '*/+' '2.2.2.2', 'INVALID', '(', ')')

        # Key: current state
        # Value: function to get str for expression
        term_str = {
            'NUM': lambda: self.get_num(),
            'OP': lambda: self.get_op(),
            'PAR_OPEN': lambda: self.open_pars(),
            'PAR_CLOSE': lambda: self.close_pars(),
            'FUNC': lambda: self.get_func(random.choice(funcs)),
            'INVALID': lambda: random.choice(invalid)
        }

        # Temporarily modify len_scale field
        stored_len = self.len_scale
        self.len_scale = len_scale

        while state != 'END':
            next_states = self.next_term_probs[state]

            # Select next state
            state = self.get_next(next_states)

            if state != 'END':
                clc_str, py_str = term_str[state]()

                # Record Operators and Functions in expression
                if state == 'OP':
                    self.ops_in_expr.add(clc_str)

                # Append next string to expression
                clc_expr.append(str(clc_str))
                py_expr.append(str(py_str))
                self.length += 1

        self.len_scale = stored_len # Revert len_scale

        return "".join(clc_expr), "".join(sympy_expr), self.length, self.ops_in_expr

    def get_next(self, next_states):
        for next in next_states:
            if random.random() <= next[1]():
                return next[0]

        return next_states[-1][0]

    def end_prob(self):
        if self.close_pars_needed > 0:
            return 0

        return self.len_scale * (1 - math.e ** (-0.1 * self.length)) ** 3

    def close_par_prob(self):
        return 1 - (math.e ** (-0.4 * self.close_pars_needed))

    def inner_func(self):
        return '()'

    def get_func(self, func):
        funcs = (
            ('sqrt(?)', 'math.sqrt(?)', 0.25),
            ('ln(?)', 'math.log(?)', 0.175),
            ('log(?)', 'math.log10(?)', 0.175),
            ('cos(?)', 'math.cos(?)', 0.1),
            ('sin(?)', 'math.sin(?)', 0.1),
            ('tan(?)', 'math.tan(?)', 0.1),
            ('cot(?)', '1 / (math.tan(?))', 0.1)
        )
        weights = [item[2] for item in funcs]
        func = random.choices(funcs, weights=weights, k=1)

        self.ops_in_expr.add(func)

        if self.len_scale < 1.5:
            return func + '(' + str(self.get_num()) + ')'

        inner_expr, inner_sympy, length, ops = self.generate_expr(self.len_scale / 3)

        return func + '(' + inner_expr + ')'

    def get_num(self):
        num = 0
        if random.random() <= 0.5:  # Return decimal 50% of the time
            num = random.randint(-50, 50)
        num = random.randrange(0, 50)
        if random.random() <= 0.15:
            num *= -1 # Return negative 15% of time
        return num

    def open_pars(self):
        self.close_pars_needed += 1
        return '('

    def close_pars(self):
        self.close_pars_needed -= 1
        return ')'

    def get_op(self):
        ops = (('+', '+', 0.25), ('-', '-', 0.25), ('*', '*', 0.2), ('/', '/', 0.2), ('^', '**', 0.1))

        # Unpack first two values (operators) and weights
        op1, op2, weights = zip(*ops)

        # Select one operator based on weights
        index = random.choices(range(len(ops)), weights=weights)[0]

        # Return both operator forms
        return op1[index], op2[index]
'''
eb = HiddenMarkov()
for i in range(10):
    expr, a, b, c = eb.generate_expr()
    print(expr)
    #print(f'Expression {i}: {eval(expr)}')
'''

print(eval('2/0'))
