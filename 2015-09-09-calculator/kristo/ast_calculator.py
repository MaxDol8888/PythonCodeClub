from operator import add, sub, mul, truediv
import re
from util import trace, pipe


@trace
def eval_basic_expr(expr):

    operand1, operand2 = re.split("[\+\-*/]", expr)
    [operation] = filter(lambda symb: symb in "*/+-", expr)

    operation = {"+": add,
                 "-": sub,
                 "*": mul,
                 "/": truediv}[operation]

    return operation(float(operand1), float(operand2))


def _get_priority_op(expr):

    def get_tier_priority_op(expr, symb):
        indxs = map(expr.find, symb)
        non_neg_indxs = filter(lambda x: x != -1, indxs)
        return min(non_neg_indxs)

    if "*" in expr or "/" in expr:
        priority_op_indx = get_tier_priority_op(expr, "*/")
    else:
        priority_op_indx = get_tier_priority_op(expr, "+-")

    return expr[priority_op_indx]


def _get_priority_scope_star_end(expr):

    start_brackets, depth_start_bracket, deepest_starting_bracket_index = 0, 0, 0

    for index, symb in enumerate(expr):
        if symb == "(":
            start_brackets += 1
        if symb == ")":
            if depth_start_bracket <= start_brackets:
                depth_start_bracket = start_brackets
                deepest_ending_bracket_index = index
            start_brackets = 0

    deepest_starting_bracket_index = expr[:deepest_ending_bracket_index].rfind("(")

    return deepest_starting_bracket_index, deepest_ending_bracket_index


@trace
def get_priority_scope(expr):

    deepest_starting_bracket_index, deepest_ending_bracket_index = _get_priority_scope_star_end(expr)

    return expr[deepest_starting_bracket_index:deepest_ending_bracket_index + 1]


@trace
def get_priority_simple_expr(expr):

    priority_operation = _get_priority_op(expr)
    priority_operation_index = expr.find(priority_operation)

    first_operand = re.split("[\+\-*/()]", expr[:priority_operation_index])[-1]
    second_operand = re.split("[\+\-*/()]", expr[priority_operation_index + 1:])[0]

    return first_operand + priority_operation + second_operand


def calc_eval(expr):

    def remove_broken_scope(expr, value):
        return expr.replace("(" + value + ")", value)

    def is_answer(expr):
        return expr.count("(") == 0

    def get_next_priority_expr(expr):
        return pipe(expr,
                    get_priority_scope,
                    get_priority_simple_expr)

    @trace
    def replace_expr(initial_expr, answ):
        indxs = _get_priority_scope_star_end(initial_expr)
        before_evaled_expr = initial_expr[:indxs[0]]
        after_evaled_expr = initial_expr[indxs[1]+1:]
        return before_evaled_expr + answ + after_evaled_expr

    if is_answer(expr):
        return float(expr)

    priority_expr = get_next_priority_expr(expr)
    priority_expr_answ = str(eval_basic_expr(priority_expr))

    new_expr = replace_expr(expr, priority_expr_answ)
    new_expr = remove_broken_scope(new_expr, priority_expr_answ)

    return calc_eval(new_expr)


if __name__ == "__main__":

    expressions = ["(2+3)",
                   "(2*(2/3)-4)",
                   # "(1+1+2-3-3-3)", Dealing with negative numbers not implemented
                   "(1+(1+1)+(1+1)+(1+(1+1))+((1+1)+1))",
                   "(2+2-4*(8-7+3+3/4))",
                   "(1+(2+(3+4))+(5+6)+(7+(8+(9+(10+11)))))"]

    for expr in expressions:
        print("\nInitial expression: ", expr)
        print("------------------------------------------------\n")
        aswr = str(calc_eval(expr))
        print("------------------------------------------------")
        print("Answer:             ", aswr)

