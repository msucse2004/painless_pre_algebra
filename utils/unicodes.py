
SUPERSCRIPT_NUMBERS = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}

SUBSCRIPT_NUMBERS = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    '10': '₁₀', '11': '₁₁', '12': '₁₂', '13': '₁₃',
    '14': '₁₄', '15': '₁₅', '16': '₁₆'
}

UNICODE_MULTIPLIER = chr(215)
UNICODE_PRODUCT = chr(8901)
UNICODE_DIVISION = chr(247)

UNICODE_SQUARE_ROOT= '\u221a'
UNICODE_PLUS_MINUS = '±'
UNICODE_DEGREE_CIRCLE = chr(176)
UNICODE_MATH_X = '𝑥'
UNITCODE_PI = chr(960)
UNICODE_THETA = chr(952)

UNICODE_BITWISE_AND = '∧'
UNICODE_BITWISE_OR = '∨'
UNICODE_BITWISE_XOR = '⊕'
UNICODE_BITWISE_NOT = '¬'

OPERATORS_MAP = ["+", "-", "*", "/", "^", UNICODE_MULTIPLIER, UNICODE_PRODUCT, UNICODE_DIVISION]
PARENTHESES = ["(", ")", "[", "]", "{", "}"]

def identify_token_type(token: str) -> str:
    if token in OPERATORS_MAP:
        return "Operator"
    elif token in PARENTHESES:
        return "Parenthesis"
    elif token in SUPERSCRIPT_NUMBERS:
        return "Superscript"
    elif token in SUBSCRIPT_NUMBERS:
        return "Subscript"
    elif token.isalnum():
        return "Number"
    else:
        return "Unknown"
