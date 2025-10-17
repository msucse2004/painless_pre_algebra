import random
from math import gcd


def is_terminating_decimal(simplified_denominator: int) -> bool:
    """분모의 소인수가 2와 5만으로 이루어져 있으면 True를 반환합니다."""
    if simplified_denominator <= 1:
        return True

    denom = simplified_denominator

    # 2로 나눌 수 있는 만큼 나눕니다.
    while denom % 2 == 0:
        denom //= 2

    # 5로 나눌 수 있는 만큼 나눕니다.
    while denom % 5 == 0:
        denom //= 5

    # 2와 5로 모두 나눈 후, 분모가 1이 되었다면 유한 소수입니다.
    return denom == 1

def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    """
    분수를 약분하여 기약분수 형태의 분자(numerator)와 분모(denominator)를 반환합니다.
    (분모가 0인 경우는 가정하지 않습니다.)
    """
    if numerator == 0:
        return 0, 1

    # 분자와 분모의 최대공약수(GCD)를 구합니다.
    common_divisor = gcd(abs(numerator), abs(denominator))

    # GCD로 분자와 분모를 나누어 약분합니다.
    new_numerator = numerator // common_divisor
    new_denominator = denominator // common_divisor

    # 분모가 음수일 경우, 분자와 분모 모두 부호를 바꿔 분모를 양수로 만듭니다.
    if new_denominator < 0:
        new_numerator *= -1
        new_denominator *= -1

    return new_numerator, new_denominator

def generate_random_fraction(geometry:dict) -> tuple:
    #geometry: type: terminating, repeating, all
    #           decimal_limit:3
    #           digit_limit: 100

    fraction_limit = geometry.get('fraction_limit', 100)  # 기본값 100
    decimal_limit = geometry.get('decimal_limit', 3)  # 기본값 3
    fraction_type = geometry.get('type', 'all').lower()


    if fraction_type == 'terminating':
        while True:
            numerator = random.randint(1, fraction_limit)
            denominator = random.randint(2, fraction_limit)
            answer = numerator / denominator
            answer_str = to_latex_decimal(numerator, denominator, decimal_limit)
            if is_terminating_decimal(answer):
                break
            elif answer_str.startswith("Error"):
                continue
    elif fraction_type == 'repeating':
        while True:
            numerator = random.randint(1, fraction_limit)
            denominator = random.randint(2, fraction_limit)
            answer = numerator / denominator
            answer_str = to_latex_decimal(numerator, denominator, decimal_limit)
            if is_terminating_decimal(answer):
                continue
            elif answer_str.startswith("Error"):
                continue
            else:
                break
    elif fraction_type == 'all':
        numerator = random.randint(1, fraction_limit)
        denominator = random.randint(2, fraction_limit)

    return numerator, denominator

def  to_latex_friction(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0"
    return f"$\\frac{{{numerator}}}{{{denominator}}}$"


def to_latex_decimal(num: int, den: int, max_number_repeating) -> str:
    """
    분수를 소수 문자열로 변환합니다. 순환 소수의 경우 LaTeX \overline{}로 표기합니다.

    분자(num)와 분모(den)는 기약분수 상태여야 합니다.
    """

    # 정수 부분
    integer_part = num // den
    remainder = num % den

    if remainder == 0:
        return str(integer_part)

    # 소수 부분 계산
    visited_remainders = {}  # (나머지: 자리수)
    decimal_digits = []
    position = 0

    while remainder != 0 and remainder not in visited_remainders:
        visited_remainders[remainder] = position

        # 다음 자리수 계산
        remainder *= 10
        digit = remainder // den
        remainder %= den

        decimal_digits.append(str(digit))
        position += 1

    decimal_str = "".join(decimal_digits)

    if remainder == 0:
        # 유한 소수
        if len(decimal_str) > max_number_repeating:
            return f"Error: decimal points is too large. {decimal_str}"
        else:
            return f"{integer_part}.{decimal_str}"
    else:
        # 순환 소수
        start_pos = visited_remainders[remainder]

        non_repeating_part = decimal_str[:start_pos]
        repeating_part = decimal_str[start_pos:]

        if  len(repeating_part)+len(non_repeating_part) > max_number_repeating:
            return f"Error: repeating part is too large. {repeating_part}"

        # LaTeX 순환 마디 표기: \overline{...} 사용
        if non_repeating_part:
            return f"{integer_part}.{non_repeating_part}$\\overline{{{repeating_part}}}$"
        else:
            return f"{integer_part}.$\\overline{{{repeating_part}}}$"