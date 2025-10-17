
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: MultiplyingFractions
Title: Multiplying Fractions
"""

import os
import sys
from fractions import Fraction

from utils import pylatex_pdf as pdf
from utils.fractions import generate_random_fraction, to_latex_friction
from utils.unicodes import UNICODE_PRODUCT


class MultiplyingFractions:
    """A class template for generating and handling math-related problems."""

    def __init__(self):
        self._title = "Multiplying Fractions"

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
        geometry_options = {"type": "all",
                            "decimal_limit": 3,
                            "fraction_limit": 10}
        numerator1, denominator1 = generate_random_fraction(geometry_options)
        numerator2, denominator2 = generate_random_fraction(geometry_options)

        problem_text = f"Multiply fractions and express in simplest form. \\\\ \\par \\qquad \\qquad {to_latex_friction(numerator1, denominator1)} $\cdot$ {to_latex_friction(numerator2, denominator2)} ="
        answer = Fraction(numerator1, denominator1) * Fraction(numerator2, denominator2)
        answer_text = f"{to_latex_friction(answer.numerator, answer.denominator)}"

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

        try:
            pdf.generate_pdf_files(f"{self._title} Problems", problem_list, num_column=2, row_spacing=400)
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=4)
            print("PDF files successfully generated.")
        except ImportError:
            print("Error: Could not find the 'pdf_handling' module. (Check utils/pdf.py module path)")
        except AttributeError:
            print("Error: 'generate_pdf_files' function is missing in the 'pdf_handling' module.")
        except Exception as e:
            print(f"Error during PDF generation: {e}")


def main():
    topic_instance = MultiplyingFractions()
    topic_instance.title = "Multiplying Fractions"
    topic_instance.generate_practice(10)


if __name__ == "__main__":
    main()
