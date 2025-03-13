import pandas as pd

class TestResults:
    def __init__(self):
        columns = ['Expression', 'Python Expression', 'clCalc Result', 'Python Result', 'Passed', 'Length']
        self.data = pd.DataFrame(columns=columns)
        ops = ['+', '-', '*', '/', '^', 'ln', 'log', 'sin', 'cos', 'tan', 'cot', 'sqrt']
        self.num_ops = pd.DataFrame({ #Holds number of operator types
            'Operators': ops,
            'In All': 0,
            'In Failed': 0
        })

    def update(self, expr, expr_p, cl_res, py_res, passed, expr_len, ops):
        self.data.loc[len(self.data)] = [expr, expr_p, cl_res, py_res, passed, expr_len]
        self.num_ops.loc[self.num_ops['Operators'].isin(ops), 'In All'] += 1
        if passed:
            self.num_ops.loc[self.num_ops['Operators'].isin(ops), 'In Failed'] += 1