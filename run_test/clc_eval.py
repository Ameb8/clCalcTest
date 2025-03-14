import re
import subprocess
from expr_result import ExprResult


def get_clc_result(expr, debug=False):
    # Pass the expression to 'clc' in the command line and capture the output
    command = f'clc "{expr}"'  # Format command for CLI execution
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        command_output = result.stdout.strip()  # Get the result from the command line
        if debug:
            print(command_output)
    except Exception as e:
        command_output = f"Could not access clCalc: {e}\nPlease check clCalc status"

    return parse_clc_output(command_output)


def parse_clc_output(output: str):
    result = ExprResult()

    # Parse clcalc output for syntax and math errors
    if "Exceeded maximum range" in output:
        return None
    if "Cannot divide by zero" in output:
        result.math_err = True
    if "Cotangent cannot be calculated" in output:
        result.math_err = True
    if "Logarithmic operations can only be paplied to postive numbers" in output:
        result.math_err = True
    if "Logarithmic operations can only be applied to positive numbers" in output:
        result.math_err = True
    if "Square root of negative numbers is not supported" in output:
        result.math_err = True
    if "Unclosed Parentheses" in output:
        result.syntax_err= True
    if "Unopened Parentheses" in output:
        result.syntax_err = True
    if "This operator requires two adjacent operands" in output or "This Operator requires one operand" in output:
        result.syntax_err= True
    if "Character not recognized" in output:
        result.syntax_err = True

    # Extract result if it's valid
    match = re.search(r"=\s*([-+]?\d*\.?\d+([eE][-+]?\d+)?)", output)
    if match:
        result.result = float(match.group(1))

    return result
