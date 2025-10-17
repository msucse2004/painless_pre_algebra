
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: WritingDecimalAsFractions
Title: Writing Decimal As Fractions
"""

import os
import random
import sys
from math import gcd

from utils import pylatex_pdf as pdf
from utils.fractions import is_terminating_decimal, simplify_fraction, to_latex_decimal


class WritingDecimalAsFractions:
    """A class template for generating and handling math-related problems."""

    def __init__(self):
        super().__init__()
        self._title = "Writing Decimal As Fractions"

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
            decimal_value = to_latex_decimal(simplified_numerator, simplified_denominator, 3)

            if decimal_value.startswith("Error"):
                continue
            elif simplified_numerator == simplified_denominator:
                continue
            elif not bool_terminating_decimal:
                continue
            else:
                break

        problem_text = f"Convert the decimal to the fraction. \\\\ \\par \\qquad \\qquad {simplified_numerator/simplified_denominator}"
        answer_text = f"$\\frac{{{simplified_numerator}}}{{{simplified_denominator}}}$"

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
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=1, row_spacing=400)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=3)
            print("PDF files successfully generated.")
        except ImportError:
            print("Error: Could not find the 'pdf_handling' module. (Check utils/pdf.py module path)")
        except AttributeError:
            print("Error: 'generate_pdf_files' function is missing in the 'pdf_handling' module.")
        except Exception as e:
            print(f"Error during PDF generation: {e}")


def main():
    topic_instance = WritingDecimalAsFractions()
    topic_instance.title = "Writing Decimal As Fractions"
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()
