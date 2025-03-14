from expr_builder import ExprBuilder
from clc_eval import get_clc_result
from test_results import TestResults
from expr_result import  get_result
from report import get_report


def evaluate_expr(expr, py_expr):
    # get results
    clcalc_result = get_clc_result(expr)
    py_result = get_result(py_expr)
    return clcalc_result, py_result


def test(num_expr):
    test_res = TestResults()
    expr_builder = ExprBuilder()

    i = 0
    while i < num_expr:
        expr, py_expr = expr_builder.get_expr() # Get generated expression
        clcalc_res, py_res = evaluate_expr(expr, py_expr)

        # Update results if ExprResults are both valid and range is not exceeded
        if py_res is not None and clcalc_res is not None: # Update test metrics
            test_res.update(expr, py_expr, clcalc_res, py_res, clcalc_res == py_res, expr_builder.total_ops, expr_builder.num_ops)
            print(f'\nTest {i+1} out of {num_expr} completed')
            i += 1

    get_report(test_res)
    return test_res

def main():
    test(1000)

if __name__ == '__main__':
    main()