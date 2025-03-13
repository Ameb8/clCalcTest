from expr_metrics import ExprMetrics
import numpy as np
import pandas as pd

class TestMetrics:
    def __init__(self, num_tests):
        self.expr_lens = np.empty(num_tests)
        self.index = 0

        self.failed_expr = []
        self.failed_clc = [] # List of clCalc results for failed expressions
        self.failed_sympy = [] # List of SymPy results for failed expressions

        self.err_rates = ExprMetrics()
        self.missed_errs = ExprMetrics()
        self.false_pos = ExprMetrics()

        ops = ['+', '-', '*', '/', '^', 'ln', 'log', 'sin', 'cos', 'tan', 'cot', 'sqrt']
        self.num_ops = pd.DataFrame({
            'Operators': ops,
            'In All': 0,
            'In Failed': 0
        })

    def update(self, clcalc_res, true_res, expr, expr_len, ops):
        # update generated expression stats
        self.err_rates.update(true_res)

        if clcalc_res != true_res: # Test failed:
            self.failed_expr.append(expr) # Track failed expressions
            self.failed_clc.append(clcalc_res)
            self.failed_sympy.append(true_res)
            expr_len *= -1 # Track lengths of error expressions
            self.update_ops(ops)
        else:
            self.update_ops(ops, True)

        # Track missed errors and false positives by clCalc
        self.false_pos.update_errs(clcalc_res, true_res)
        self.missed_errs.update_errs(true_res, clcalc_res)
        self.update_ops(ops)

        self.expr_lens[self.index] = expr_len # Update expression lengths list
        self.index += 1

    def __str__(self):
        output = []
        output.append(f'\nTest Cases Passed: {len(self.expr_lens) - len(self.failed_expr)}/{len(self.expr_lens)} ')
        output.append(f'Errors Missed by clCalc:\n{self.missed_errs}')
        output.append(f'False Positives by clCalc:\n{self.false_pos}')
        output.append('Generated Expression Statistics:')
        output.append(f'Average Length: {np.mean(np.abs(self.expr_lens))}')
        output.append(f'Median Length: {np.median(np.abs(self.expr_lens))}')
        output.append(f'Standard Deviation: {np.std(np.abs(self.expr_lens))}')
        output.append(f'Shortest Expression: {np.min(np.abs(self.expr_lens))}')
        output.append(f'Longest Expression:{np.max(np.abs(self.expr_lens))}')
        output.append(f'Expressions With Errors:\n{self.err_rates}')
        if len(self.failed_expr) > 0:
            failed = '\n'.join(self.failed_expr)
            output.append(f'Failed Expressions: \n{failed}')

        return '\n'.join(output)

    def num_tests(self):
        return len(self.expr_lens)

    def update_ops(self, ops, err=False):
        for op in ops:
            self.num_ops.loc[self.num_ops["Operators"] == op, "In All"] += 1
            if err:
                self.num_ops.loc[self.num_ops["Operators"] == op, "In Failed"] += 1
