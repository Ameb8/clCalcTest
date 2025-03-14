import pandas as pd

class TestResults:
    def __init__(self):
        columns = ['Expression', 'Python Expression', 'clCalc Result', 'Python Result', 'Passed', 'Length']
        self.num_failed = 0
        self.data = pd.DataFrame(columns=columns)
        ops = ['+', '-', '*', '/', '^', 'ln', 'log_10', 'sin', 'cos', 'tan', 'cot', '√']
        self.num_ops = pd.DataFrame({ #Holds number of operator types
            'Operators': ops,
            'In All': 0,
            'In Failed': 0
        })
        self.errors = pd.DataFrame({ # Tracks Errors and recognition statistics
            'No Error': [0, 0, 0],
            'Math Error': [0, 0, 0],
            'Syntax Error': [0, 0, 0]
        }, index=['No Error', 'Math Error', 'Syntax Error'])

    def update(self, expr, expr_p, cl_res, py_res, passed, expr_len, ops):
        self.data.loc[len(self.data)] = [expr, expr_p, cl_res, py_res, passed, expr_len]
        self.num_ops.loc[self.num_ops['Operators'].isin(ops), 'In All'] += 1
        if not passed:
            self.num_ops.loc[self.num_ops['Operators'].isin(ops), 'In Failed'] += 1
            self.num_failed += 1
        self.update_errors(cl_res, py_res)

    # Complicated structure to account for clCalc's ability to ignore some syntax errors during evaluation
    def update_errors(self, clc_result, py_result):
        row = 'No Error'
        col = 'No Error'
        # Determine the Python result category (actual result)
        if py_result.math_err:
            row = 'Math Error'
            if clc_result.math_err:
                col = 'Math Error'
            elif clc_result.syntax_err:
                col = 'Syntax Error'
        elif py_result.syntax_err:
            row = 'Syntax Error'
            if clc_result.syntax_err:
                col = 'Syntax Error'
            elif clc_result.math_err:
                col = 'Math Error'
        else:
            row = 'No Error'
            if clc_result.math_err:
                col = 'Math Error'
            elif clc_result.syntax_err:
                col = 'Syntax Error'

        self.errors.loc[row, col] += 1
