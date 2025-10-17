
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: AddingAndSubtractingFractions
Title: Adding And Subtracting Fractions
"""

import os
import random
import sys
from fractions import Fraction

from utils import pylatex_pdf as pdf
from utils.fractions import to_latex_friction, simplify_fraction


class AddingAndSubtractingFractions:
    """A class template for generating and handling math-related problems."""

    def __init__(self):
        self._title = "Adding And Subtracting Fractions"

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
        numerator1 = random.randint(2, 20)
        denominator1 = random.randint(2, 20)

        numerator2 = random.randint(2, 20)
        denominator2 = random.randint(2, 20)

        fraction1 = Fraction(numerator1, denominator1)
        fraction2 = Fraction(numerator2, denominator2)

        random_operator = random.choice(["+", "-"])

        if random_operator == "+":
            answer = fraction1 + fraction2
            simplified_answer_numerator, simplied_answer_denominator = simplify_fraction(answer.numerator, answer.denominator)
            problem_text = f"Add fractions and simplify if possible. \\\\ \\par \\qquad \\qquad {to_latex_friction(numerator1, denominator1)} + {to_latex_friction(numerator2, denominator2)} ="
        else:
            answer = fraction1 - fraction2
            simplified_answer_numerator, simplied_answer_denominator = simplify_fraction(answer.numerator,
                                                                                                    answer.denominator)
            problem_text = f"Subtract fractions and simplify if possible. \\\\ \\par \\qquad \\qquad {to_latex_friction(numerator1, denominator1)} - {to_latex_friction(numerator2, denominator2)} ="
        answer_text = f"{to_latex_friction(simplified_answer_numerator, simplied_answer_denominator)}"
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
    topic_instance = AddingAndSubtractingFractions()
    topic_instance.title = "Adding And Subtracting Fractions"
    topic_instance.generate_practice(10)


if __name__ == "__main__":
    main()
