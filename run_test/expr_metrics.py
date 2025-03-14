class ExprMetrics:
    def __init__(self):
        self.math_errs = 0
        self.syntax_errs = 0

    # Updates metrics with expression errors
    def update(self, result):
        if result.math_err:
            self.math_errs += 1
        if result.syntax_err:
            self.syntax_errs += 1

    def update_errs(self, res_1, res_2):
        if res_1.math_err and not res_2.math_err:
            self.math_errs += 1

        if res_1.syntax_err and not res_2.syntax_err:
            self.syntax_errs += 1

    def __str__(self):
        nonzero_fields = {field: value for field, value in vars(self).items() if value > 0}

        if nonzero_fields:
            return "\n".join(f"\t{field}: {value}" for field, value in nonzero_fields.items())
        else:
            return "\tNo errors"

