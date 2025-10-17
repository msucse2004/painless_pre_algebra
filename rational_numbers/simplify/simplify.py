
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: Simplify
Title: Simplify
"""

import os
import random
import sys

from utils import pylatex_pdf as pdf
from math import gcd

from utils.fractions import simplify_fraction


class Simplify:
    """A class template for generating and handling math-related problems."""

    def __init__(self) -> None:
        self._title = "Simplify"

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
        gcd_value = 1
        while gcd_value == 1:
            numerator = random.randint(1, 300)
            denominator = random.randint(1, 300)
            gcd_value = gcd(numerator, denominator)

        answer_numerator, answer_denomirator = simplify_fraction(numerator, denominator)
        problem_text = (f"Simplify fractions: \\\\ \\par \\qquad \\qquad"
                        f"$\\frac{{{numerator}}}{{{denominator}}}$")
        answer_text = f"$\\frac{{{answer_numerator}}}{{{answer_denomirator}}}$"
        #answer_text = f"{answer_numerator}/{answer_denomirator}"
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
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=5)
            print("PDF files successfully generated.")
        except ImportError:
            print("Error: Could not find the 'utils.pylatex_pdf' module.")
        except AttributeError:
            # 이 메시지는 실제로 발생해서는 안 되지만, 디버깅을 위해 남겨둡니다.
            print("Error: 'generate_pdf_files' function is missing in the 'utils.pylatex_pdf' module.")
        except Exception as e:
            print(f"Error during PDF generation: {e}")


def main():
    topic_instance = Simplify()
    topic_instance.title = "Simplify"
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()
