from .test_clcalc import test
from .report import get_report

def main():
    print('Welcome to clCalcTest')
    while run_test():
        pass

def run_test():
    num_expr = 0
    while num_expr <= 0:
        try:
            user_in = input('Please enter the number of expressions you would like to test, or press enter to exit: ')
            if user_in == '':
                return False
            num_expr = int(user_in)
        except (ValueError, Exception):
            print('Please enter an integer value greater than zero')

    test_result = test(num_expr)
    get_report(test_result)

if __name__ == '__main__':
    main()