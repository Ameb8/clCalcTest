import sympy as sp
from sympy import sympify, I, SympifyError
from expr_result import ExprResult
import multiprocessing
import logging

# Number of seconds for SymPy to process before termination
TIMEOUT = 3

def check_expr_inner(expr, return_dict, debug):
    result = ExprResult() # Holds evaluation data

    try:
        # Convert the string expression to a SymPy expression
        expr = sp.sympify(expr)

        try:# Simplify the expression to check for specific cases
            simplified_expr = sp.simplify(expr)

            # Check if SymPy simplified expression has zoo or pi
            if simplified_expr.has(sp.zoo) or simplified_expr.has(sp.I):
             result.math_err = True

            # Check for i in evaluated expression
            # Require for when operand of log or sqrt is irrational and evaluates to a negative
            expr = simplified_expr.evalf()
            if expr.has(sp.I) or expr.has(sp.zoo):
                    result.math_err = True
            # Check if the simplified expression is purely a number and convert to Python type
            elif simplified_expr.is_number and simplified_expr.is_real:
                result.result = simplified_expr.evalf()

            if debug:
                return_dict['simplified'] = simplified_expr
                return_dict['evalf'] = expr

        except Exception as e: # Catch imaginary numbers
            result.math_err = True
    except SympifyError as e: # Syntax error caught
        result.syntax_err = True
    finally: # 'Return' result
        return_dict['result'] = result


# Wrapper function for SymPy evaluation.
# With large numbers, SymPy attempts to evaluate for long periods of time
# Terminates process if runtime is greater than 'TIMEOUT' constant
def check_expr(expr, debug=False):
    # Create a dictionary to hold the result from the subprocess
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # Create a subprocess to run the function
    process = multiprocessing.Process(target=check_expr_inner, args=(expr, return_dict, debug))

    # Start the process
    process.start()

    # Wait for the process to finish or timeout
    process.join(TIMEOUT)

    # If process is still running, terminate it
    if process.is_alive():
        process.terminate()
        process.join()
        return None

    if debug:
        print(f'simplified expression: {return_dict.get('simplified')}')
        print(f'evaluated expression: {return_dict.get('evalf')}')
        print(f'expression result: {return_dict.get('result')}')

    # Return the result if available
    return return_dict.get("result", None)


def main():
    # print(f"'sqrt(cos(ln(28))': {check_expr('sqrt(cos(ln(28))')}")
    '''
    r_dict = {}
    print(f'sqrt(cos(ln(28))): {check_expr_inner('sqrt(cos(ln(28)))', r_dict)}')
    print(r_dict.get("result", None))
    print(f"simplified expression: {r_dict.get('simplified')}")
    '''
    res = check_expr('32^cot(-24)^19--41+-10^-17+26', True)
    print(f'Result: {res.result}')
    print(f'Math Error: {res.math_err}')
    print(f'Syntax Error: {res.syntax_err}')
    # print(check_expr('cos(ln(28))', True))


if __name__ == '__main__':
    main()