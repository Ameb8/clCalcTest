from expr_builder import ExprBuilder
from clc_eval import get_clc_result
from test_results import TestResults
from expr_result import  get_result

# Gets results for inputted expression
def evaluate_expr(expr, py_expr):
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
            if (i + 1) % 10 == 0:
                print(f'\nTest {i+1} out of {num_expr} completed')
            i += 1

    print('Test Completed')
    print(f'{len(test_res.data) - test_res.num_failed} out of {len(test_res.data)} Test Cases Passed')

    return test_res