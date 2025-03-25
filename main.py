# version=1.0.2
# coding=utf-8

"""
Something new:
    Can put some plus signs or minus signs before terms.
"""


numbers = list('0123456789')
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ''abcdefghijklmnopqrstuvwxyz')
division = ['/']
primary = ['+', '-']
equal = ['=']
space = [' ']
terms = numbers + alphabet + division
operators = primary + equal
chars = terms + operators + space
errors = {
    'E0000': '\nWrong number of equal signs.',
    'E0001': '\nNot followed by a space after an unknown number.',
    'E0002': '\nIllegal characters.',
    'E0003': '\nNo unknowns.',
    'E0004': '\nAn operator after the equation.',
    'E0005': '\nWrong number of division sign in the term.',
    'E0006': '\nThe term has any operators.',
    'E0007': '\nWrong character beside division sign.',
    'E0008': '\nOperator error.',
    'E0101': 'The number of equations does not equal to the number of unknowns.',
    'E0102': 'Coefficient error.'
}


def put_spaces(equation: str, sep=None):
    if sep is None:
        sep = operators
    equation = equation.split(' ')
    text = ''
    for string in equation:
        text += string
    equation = text
    is_operator = True
    i = 0
    while i < len(equation):
        if not equation[i] in sep:
            is_operator = False
        elif not is_operator:
            is_operator = True
            equation = f'{equation[:i]} {equation[i]} {equation[i + 1:]}'
            i += 2
        i += 1
    return equation


def prepare():
    print('Please write a system of linear equations.\n'
          'Do not put irrationals. Put fractions before the unknowns.\n'
          'Do not use decimals.\n'
          'Do not use the multiple sign and the pair of parentheses.\n'
          'Press Enter again to solve.\n'
          'Equations:\n')
    return [], [], [], put_spaces(input())


def error(code: str, errors_dict=None):
    if errors_dict is None:
        errors_dict = errors
    print(f'{errors_dict[code]}({code})')
    input()
    exit()


def check_string(equation: str):
    if equation.count('=') != 1:
        error('E0000')
    unknown_list = []
    is_unk = False
    for char in equation:
        if char not in chars:
            error('E0002')
        if (char != ' ') and is_unk:
            error('E0001')
        if char not in alphabet:
            is_unk = False
        else:
            unknown_list.append(char)
            is_unk = True
    if not unknown_list:
        error('E0003')
    return unknown_list


def check_strings_between_spaces(equation: str):
    equation_list = equation.split(' ')
    if not equation_list[-1]:
        error('E0004')
    for terms_or_operators in equation_list:
        if terms_or_operators.count('/') > 1:
            error('E0005')
    return equation_list


def check_char_beside_division(char: str, string: str):
    if char == '/' and (string.index('/') + 1 == len(string) or string[string.index('/') + 1] not in numbers[1:]
                        or not string.index('/') or string[string.index('/') - 1] not in numbers):
        error('E0007')


def check_terms(string_term: str):
    for char in string_term:
        error('E0006') if char == '=' else check_char_beside_division(char, string_term)


def check_first_terms(string_term: str):
    for char in string_term:
        if char not in primary:
            break
    else:
        error('E0006')
    check_terms(string_term)


def check_signs(string_sign: str):
    error('E0008') if string_sign not in operators else None


def check_equation(equation_list: list):
    is_first_term = True
    is_sign = False
    for terms_or_operators in equation_list:
        if is_sign:
            check_signs(terms_or_operators)
            if terms_or_operators == '=':
                is_first_term = True
            is_sign = False
        else:
            if is_first_term:
                check_first_terms(terms_or_operators)
                is_first_term = False
            else:
                check_terms(terms_or_operators)
            is_sign = True


def append_new(new_equation: str, new_unknowns: list, new_equ_list: list,
               equations_list: list, unknowns_list: list, sys_equ_list: list):
    equations_list.append(new_equation)
    for unk in new_unknowns:
        unknowns_list.append(unk)
    sys_equ_list.append(new_equ_list)


def input_equation(equation: str, equations_list: list, unknowns_list: list, sys_equ_list: list):
    unknown = check_string(equation)
    equation_list = check_strings_between_spaces(equation)
    check_equation(equation_list)
    append_new(equation, unknown, equation_list, equations_list, unknowns_list, sys_equ_list)
    return put_spaces(input())


def check_number_equations_unknowns(equations_list: list, unknowns_list: list):
    unknowns_list = sorted(list(set(unknowns_list)), key=lambda letter: alphabet.index(letter))
    if len(equations_list) != len(unknowns_list):
        error('E0101')
    return unknowns_list


def unite_terms_operators(sys_equ_list: list):
    equation_list = []
    for equation in sys_equ_list:
        terms_or_operators_list = []
        string_term = ''
        for string in equation:
            if string in operators:
                if string == '-':
                    string_term = string
                if string == '=':
                    terms_or_operators_list.append(string)
            else:
                for i in range(len(string)):
                    if string[i] not in primary:
                        string_term += string[i:]
                        break
                    elif string[i] == '-':
                        string_term = '' if string_term else '-'
                terms_or_operators_list.append(string_term)
                string_term = ''
        equation_list.append(terms_or_operators_list)
    return equation_list.copy()


def move_terms(sys_equ_list: list):
    equation_list = []
    for equation in sys_equ_list:
        will_move_term = [[], []]
        after_equ = False
        for string in equation:
            if string == '=':
                after_equ = True
            else:
                t_i_a = string[-1] in alphabet
                if t_i_a if after_equ else (not t_i_a):
                    will_move_term[0 if after_equ else 1].append(string)
        after_equ = False
        for side in will_move_term:
            for string in side:
                for i in range(len(equation)):
                    if equation[i] == string and int(i > equation.index('=')) + int(after_equ) == 1:
                        equation.pop(i)
                        break
                equation.insert(int(after_equ) * len(equation), string[1:] if string[0] == '-' else '-' + string)
            after_equ = True
        equation_list.append(equation)
    return equation_list.copy()


def factorization(num: int):
    if num == 1:
        return []
    primes = []
    for i in range(2, num + 1):
        for j in range(2, int(i ** 0.5) + 1):
            if i / j % 1 == 0:
                break
        else:
            primes.append(i)
    factors = []
    while num not in primes:
        for prime in primes:
            if num / prime % 1 == 0:
                num = int(num / prime)
                factors.append(prime)
                break
    factors.append(num)
    return factors


def reduction(fraction: list):
    if fraction[0] == 0:
        return '0'
    plus_or_minus = int(abs(fraction[0]) * abs(fraction[1]) / fraction[0] / fraction[1])
    fraction[0] = abs(fraction[0])
    fraction[1] = abs(fraction[1])
    numerator = factorization(fraction[0])
    denominator = factorization(fraction[1])
    will_move_factor = []
    for factor_numerator in numerator:
        for factor_denominator in denominator:
            if factor_numerator == factor_denominator:
                will_move_factor.append(factor_numerator)
                denominator.remove(factor_denominator)
                break
    for factor in will_move_factor:
        numerator.remove(factor)
    if len(numerator):
        while len(numerator) > 1:
            numerator.insert(0, numerator.pop(0) * numerator.pop(0))
        numerator = numerator[0]
    else:
        numerator = 1
    if len(denominator):
        while len(denominator) > 1:
            denominator.insert(0, denominator.pop(0) * denominator.pop(0))
        denominator = denominator[0]
    else:
        denominator = 1
    if denominator == 1:
        return str(numerator * plus_or_minus)
    return str(numerator * plus_or_minus) + '/' + str(denominator)


def plus_string(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    return str(int(num1[0]) * int(num2[1]) + int(num1[1]) * int(num2[0])) + '/' + str(int(num1[1]) * int(num2[1]))


def num_list(nums: list):
    plus_list = nums
    while len(plus_list) > 1:
        plus_list.insert(0, plus_string(plus_list.pop(0), plus_list.pop(0)))
    return reduction([int(plus_list[0].split('/')[0]),
                     int(plus_list[0].split('/')[1] if ('/' in plus_list[0]) else '1')])


def unite_terms(sys_equ_list: list, unknowns_list: list):
    equation_list = []
    for equation in sys_equ_list:
        ind = equation.index('=')
        equation_left = equation[:ind]
        equation_right = equation[ind + 1:]
        will_unite_coefficient = []
        will_unite_unknown = []
        for string in equation_left:
            if string[-1] not in will_unite_unknown:
                will_unite_unknown.append(string[-1])
                will_unite_coefficient.append([string[:-1] + ('' if string[:-1] and string[:-1] != '-' else '1')])
            else:
                will_unite_coefficient[will_unite_unknown.index(string[-1])].append(
                    string[:-1] + ('' if string[:-1] and string[:-1] != '-' else '1'))
        for i in range(len(will_unite_coefficient)):
            will_unite_coefficient[i] = num_list(will_unite_coefficient[i])
        equation_left = list(zip(will_unite_coefficient, will_unite_unknown))
        for unk in unknowns_list:
            if unk not in will_unite_unknown:
                equation_left.append(('0', unk))
        equation_left = sorted(equation_left, key=lambda item: unknowns_list.index(item[1]))
        for i in range(len(equation_left)):
            equation_left[i] = equation_left[i][0]
        equation_right = num_list(equation_right) if equation_right else '0'
        equation_list.append([equation_left, equation_right])
    return equation_list.copy()


def multiple(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = reduction([int(num1[0]) * int(num2[0]), int(num1[1]) * int(num2[1])])
    return num


def coefficient_elimination(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num1.reverse()
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = reduction([int(num1[0]) * int(num2[0]) * -1, int(num1[1]) * int(num2[1])])
    return num


def equality_property(equation: list, multiplier: str):
    equation_list = [[]]
    for i in range(len(equation[0])):
        equation_list[0].append(multiple(equation[0][i], multiplier))
    equation_list.append(multiple(equation[1], multiplier))
    return equation_list


def plus_equation(equation1: list, equation2: list):
    equation = [[]]
    for i in range(len(equation1[0])):
        equation[0].append(num_list([equation1[0][i], equation2[0][i]]))
    equation.append(num_list([equation1[1], equation2[1]]))
    return equation


def gaussian_elimination(sys_equ_list: list, unknowns_list: list):
    for i in range(len(unknowns_list) - 1):
        for j in range(i, len(unknowns_list)):
            for k in range(i, len(unknowns_list)):
                if sys_equ_list[k][0][j] != '0':
                    break
            else:
                error('E0102')
        for j in range(i, len(unknowns_list)):
            if sys_equ_list[j][0][i] != '0':
                sys_equ_list.insert(i, sys_equ_list.pop(j))
                break
        for j in range(i + 1, len(unknowns_list)):
            sys_equ_list[j] = plus_equation(sys_equ_list[j], equality_property(
                sys_equ_list[i], coefficient_elimination(sys_equ_list[i][0][i], sys_equ_list[j][0][i])))
    return sys_equ_list


def divided(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num1.reverse()
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = reduction([int(num1[0]) * int(num2[0]), int(num1[1]) * int(num2[1])])
    return num


def minus_two_string(num1: str, num2: str):
    num1 = num1.split('/') if ('/' in num1) else [num1, '1']
    num2 = num2.split('/') if ('/' in num2) else [num2, '1']
    num = reduction([int(num1[0]) * int(num2[1]) - int(num1[1]) * int(num2[0]), int(num1[1]) * int(num2[1])])
    return num


def solve_equations(sys_equ_list: list, unknowns_list: list):
    equation_list = []
    for i in range(len(unknowns_list)):
        for j in range(i):
            sys_equ_list[-i - 1][1] = minus_two_string(sys_equ_list[-i - 1][1],
                                                       multiple(sys_equ_list[-i - 1][0].pop(), equation_list[-j - 1]))
        error('E0102') if sys_equ_list[-i - 1][0][-1] == '0' \
            else equation_list.insert(0, divided(sys_equ_list[-i - 1][0][-1], sys_equ_list[-i - 1][1]))
    for i in range(len(equation_list)):
        equation_list[i] = unknowns_list[i] + ' = ' + equation_list[i]
    return equation_list.copy()


def print_it(things: list):
    for thing in things:
        print(thing)


if __name__ == '__main__':
    equations, unknowns, sys_equ, equ = prepare()

    while equ:
        equ = input_equation(equ, equations, unknowns, sys_equ)

    unknowns = check_number_equations_unknowns(equations, unknowns)

    # print(equations)
    # print(unknowns)
    # print(sys_equ)

    sys_equ = unite_terms_operators(sys_equ)

    # print(sys_equ)

    sys_equ = move_terms(sys_equ)

    # print(sys_equ)

    sys_equ = unite_terms(sys_equ, unknowns)

    # print(sys_equ)

    sys_equ = gaussian_elimination(sys_equ, unknowns)

    # print(sys_equ)

    sys_equ = solve_equations(sys_equ, unknowns)

    print_it(sys_equ)
    input()
