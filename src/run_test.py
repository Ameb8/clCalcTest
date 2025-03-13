from hidden_markov import HiddenMarkov
from clc_eval import get_clc_result
from sympy_eval import check_expr
from test_metrics import TestMetrics
from report_results import get_report


def evaluate_expr(expr, sympy_expr):
    # get results
    sympy_result = check_expr(sympy_expr)
    clc_result = get_clc_result(expr)

    return sympy_result, clc_result


def test(num_expr):
    test_metrics = TestMetrics(num_expr)
    expr_builder = HiddenMarkov()

    i = 0 # use i explicitly to dynamically control iterations
    while i < num_expr:
        expr, expr_len, expr_items = expr_builder.generate_expr() # Get generated expression
        sympy_res, clcalc_res = evaluate_expr(expr, expr) # Evaluate expression

        # Update results if ExprResults are both valid and range is not exceeded
        if sympy_res is not None and clcalc_res is not None: #Update test metrics
            test_metrics.update(clcalc_res, sympy_res, expr, expr_len, expr_items)
            print(f'\nTest {i+1} out of {num_expr} completed')
            i += 1

    get_report(test_metrics, debug=True)

def main():
    test(100)

if __name__ == '__main__':
    main()

