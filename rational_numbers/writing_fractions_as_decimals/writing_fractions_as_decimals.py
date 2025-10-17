
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: WritingFractionsAsDecimals
Title: Writing Fractions As Decimals
"""

import os
import random
import sys
from math import gcd

from utils import pylatex_pdf as pdf
from utils.fractions import is_terminating_decimal, simplify_fraction


class WritingFractionsAsDecimals:
    """A class template for generating and handling math-related problems."""

    def __init__(self):
        self._title = "Writing Fractions As Decimals"
        self._max_number_repeating = 4

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

    def to_decimal_string(self, num: int, den: int) -> str:
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
            if len(decimal_str) > self._max_number_repeating:
                return f"Error: decimal points is too large. {decimal_str}"
            else:
                return f"{integer_part}.{decimal_str}"
        else:
            # 순환 소수
            start_pos = visited_remainders[remainder]

            non_repeating_part = decimal_str[:start_pos]
            repeating_part = decimal_str[start_pos:]

            if  len(repeating_part)+len(non_repeating_part) > self._max_number_repeating:
                return f"Error: repeating part is too large. {repeating_part}"

            # LaTeX 순환 마디 표기: \overline{...} 사용
            if non_repeating_part:
                return f"{integer_part}.{non_repeating_part}$\\overline{{{repeating_part}}}$"
            else:
                return f"{integer_part}.$\\overline{{{repeating_part}}}$"


    def generate_problem(self) -> tuple[str, str]:
        """
        Generates a single problem and its corresponding answer.
        Returns: (problem_text, answer_text)
        """
        problem_text, answer_text = None, None

        while True:
            numerator = random.randint(1, 100)
            bool_negation = random.choice([True, False])

            if bool_negation:
                numerator *= -1

            denominator = random.randint(2, 100)

            gcd_value = gcd(numerator, denominator)

            simplified_numerator, simplified_denominator =  simplify_fraction(numerator, denominator)


            bool_terminating_decimal = is_terminating_decimal(simplified_denominator)

            decimal_type = "terminating decimal" if bool_terminating_decimal else "repeating decimal"
            decimal_value = self.to_decimal_string(simplified_numerator, simplified_denominator)

            if decimal_value.startswith("Error"):
                continue
            elif numerator == denominator:
                continue
            else:
                break

        problem_text = f"Convert the fraction to a decimal, and determine the type of decimal: \\\\ \\par \\qquad \\qquad $\\frac{{{numerator}}}{{{denominator}}}$"
        answer_text = f"{decimal_value}, {decimal_type}"

        # Implement the problem generation logic here.

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

        # PDF file path setup
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        module_path = os.path.join(parent_dir, "pdf_handling")

        if module_path not in sys.path:
            sys.path.append(module_path)

        try:
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=1, row_spacing=600)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=2)
            print("PDF files successfully generated.")
        except ImportError:
            print("Error: Could not find the 'pdf_handling' module. (Check utils/pdf.py module path)")
        except AttributeError:
            print("Error: 'generate_pdf_files' function is missing in the 'pdf_handling' module.")
        except Exception as e:
            print(f"Error during PDF generation: {e}")


def main():
    topic_instance = WritingFractionsAsDecimals()
    topic_instance.title = "Writing Fractions As Decimals"
    topic_instance.generate_practice(50)


if __name__ == "__main__":
    main()
