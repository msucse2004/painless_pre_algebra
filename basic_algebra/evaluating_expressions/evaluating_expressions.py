
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: EvaluatingExpressions
Title: Evaluating Expressions
"""

import os
import random
import sys
from fractions import Fraction

from utils import pylatex_pdf as pdf


class EvaluatingExpressions:
    """A class template for generating and handling math-related problems."""
    _TEMPLATE = {
        # 단일 변수 기본 연산 (x, m, z, r, y에 대한)
        1: [{'problem': "${0}x + {1}\\ for\\ x = {2}$", 'expression': '{0}*{2}+{1}'},
            {'problem': "${0} - {1}m\\ for\\ m = {2}$", 'expression': '{0}-{1}*{2}'},
            {'problem': "${0}(z + {1})\\ for\\ z = {2}$", 'expression': '{0}*({2} + {1})'},  # z = {2} 대입
            {'problem': "${0}({1} + x) + 5\\ for\\ x = {2}$", 'expression': '{0}*({1} + {2}) + 5'},  # x = {2} 대입
            {'problem': "$\\frac{{({0}y - {1})}} {{{2}}}\\ for\\ y = {3}$", 'expression': '({0}*{3} - {1}) / {2}'},  # y = {3} 대입
            {'problem': "${0}r^2 + {1}\\ for\\ r = {2}$", 'expression': '{0}*({2}**2) + {1}'}  # r = {2} 대입
            ],

        # 다중 변수 기본 연산 (z, y, a, b, p, q, k, j에 대한)
        2: [{'problem': "${0}z - {1}y + {2}\\ for\\ z = {3}, y = {4}$", 'expression': '{0}*{3} - {1}*{4} + {2}'},
            {'problem': "${0}a + {1}b - {2}\\ for\\ a = {3}, b = {4}$", 'expression': '{0}*{3} + {1}*{4} - {2}'},
            {'problem': "${0}(p + {1}) + {2}q\\ for\\ p = {3}, q = {4}$", 'expression': '{0}*({3} + {1}) + {2}*{4}'},
            {'problem': "$\\frac {{({0}k - {1}j)}} {{{2}}}\\ for\\ k = {3}, j = {4}$", 'expression': '({0}*{3} - {1}*{4}) / {2}'}
            ],

        # 고차항 및 분수 (s, t, v, x, m에 대한)
        3: [{'problem': "${0}s^2 + {1}t - {2}\\ for\\ s = {3}, t = {4}$", 'expression': '{0}*({3}**2) + {1}*{4} - {2}'},
            {'problem': "${0}v^2 + {1}v + {2}\\ for\\ v = {3}$", 'expression': '{0}*({3}**2) + {1}*{3} + {2}'},
            {'problem': "$\\frac{{(x + {0})}}{{{1}}} + {2}\\ for\\ x = {3}$", 'expression': '({3} + {0}) / {1} + {2}'},
            {'problem': "$\\frac{{{0}}}{{m}} * {1} + {2}\\ for\\ m = {3}$", 'expression': '({0}/{3}) * {1} + {2}'}
            ],
    }

    def __init__(self):
        self._title = "Evaluating Expressions"

    @property
    def title(self):
        """Returns the title of the problem type."""
        return self._title

    @title.setter
    def title(self, value):
        """Sets the title of the problem type."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")
        self._title = value

    def generate_problem(self) -> tuple[str, str]:
        """
        Generates a single problem and its corresponding answer.
        Returns: (problem_text, answer_text)
        """
        problem_text, answer_text = None, None

        # Implement the problem generation logic here.
        templete_key = random.choice(list(self._TEMPLATE.keys()))
        #non_zero_range = list(range(-9, -1)) + list(range(2, 10))
        non_zero_range = list(range(2, 10))
        terms = [random.choice(non_zero_range) for _ in range(10)]
        str_terms = [str(t) for t in terms]
        fraction_terms = [f"Fraction({t})" for t in terms]

        keyword_template = random.choice(self._TEMPLATE[templete_key])

        try:
            problem_text = f"Evaluate following expression with given value(s). \\\\ \\par \\qquad {keyword_template['problem'].format(*str_terms)}"
        except IndexError as e:
            print(f"Error formatting template : {e}")
            return None, None

        try:
            expression_to_evaluate = keyword_template['expression'].format(*fraction_terms)
            #expression_to_evaluate = '(-5*8 - -2) / 3'
            #expression_to_evaluate = 'Fraction(4)'
            result_fraction = eval(expression_to_evaluate, {'Fraction': Fraction})

            # 분모가 1이면 정수로 출력 (예: 5/1 -> 5)
            if result_fraction.denominator == 1:
                answer_text = str(result_fraction.numerator)
            # 분모가 -1이면 부호를 분자로 올려서 정수로 출력 (예: -5/-1 -> 5)
            elif result_fraction.denominator == -1:
                answer_text = str(-result_fraction.numerator)
            # 그 외는 기약분수 형태로 출력 (예: 5/3, -5/3)
            else:
                answer_text = f"$\\frac{{{result_fraction.numerator}}}{{{result_fraction.denominator}}}$"

        except ZeroDivisionError:
            # 0으로 나누기 오류가 발생하면 무효 처리
            return None, None
        except Exception as e:
            # 기타 계산 오류 발생 시
            print(f"Calculation Error for expression '{expression_to_evaluate}': {e}")
            return None, None


        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        """Fetches a newly generated problem and logs it."""
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_problem()
        print(f"Problem: {problem_text} | Answer: {answer_text}")

        return problem_text, answer_text

    def generate_practice(self, number_of_problems: int = 10):
        """Generates a specified number of problems and saves them as PDF files."""
        num_of_problems = 0
        problem_list = []
        answer_list = []

        while num_of_problems < number_of_problems:
            problem, answer = self.get_problem_answer()
            if problem and answer:  # Only append valid problem/answer pairs
                problem_list.append(problem)
                answer_list.append(answer)
                num_of_problems += 1
            else:
                print("Warning: Failed to generate a valid problem/answer. Retrying.")

        try:
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=1, row_spacing=400)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=4)
            print("PDF files successfully generated.")
        except ImportError:
            print("Error: Could not find the 'pdf_handling' module. (Check utils/pdf.py module path)")
        except AttributeError:
            print("Error: 'generate_pdf_files' function is missing in the 'pdf_handling' module.")
        except Exception as e:
            print(f"Error during PDF generation: {e}")


def main():
    topic_instance = EvaluatingExpressions()
    topic_instance.title = "Evaluating Expressions"
    topic_instance.generate_practice(10)


if __name__ == "__main__":
    main()
