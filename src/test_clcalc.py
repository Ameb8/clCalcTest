from expr_builder import ExprBuilder
from clc_eval import get_clc_result
from sympy_eval import check_expr
from test_results import TestResults
from report_results import get_report


def evaluate_expr(expr, sympy_expr):
    # get results
    sympy_result = check_expr(sympy_expr)
    clc_result = get_clc_result(expr)

    return sympy_result, clc_result


def test(num_expr):
    test_res = TestResults()
    expr_builder = ExprBuilder()

    i = 0 # use i explicitly to dynamically control iterations
    while i < num_expr:
        expr, py_expr, expr_len, expr_items = expr_builder.get_expr() # Get generated expression
        py_res, clcalc_res = evaluate_expr(expr, expr) # Evaluate expression

#     def update(self, expr, expr_p, cl_res, py_res, passed, expr_len, ops)

        # Update results if ExprResults are both valid and range is not exceeded
        if py_res is not None and clcalc_res is not None: # Update test metrics
            test_res.update(expr, py_expr, clcalc_res, py_res, clcalc_res == py_res, expr_len, expr_items)
            print(f'\nTest {i+1} out of {num_expr} completed')
            i += 1

    get_report(test_res, debug=True)

def main():
    test(100)

if __name__ == '__main__':
    main()