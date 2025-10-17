import os
import random
import sys

from utils import pylatex_pdf as pdf


class OneStepEquations:
    """A class template for generating and handling math-related problems."""

    _VARIABLES = ['x', 'y', 'm', 'z']

    _PROBLEM_TEMPLATES = {
        # A * V = C  (e.g., 6x = 24. Solution: x = 4)
        'multiplication': {
            'problem': "${0}{1} = {2}$",  # {0}=A, {1}=V, {2}=C
            'answer': "{1} = {3}"  # {1}=V, {3}=X (Solution)
        },
        # V / A = C or (V / A) = C (LaTeX: \frac{V}{A} = C) (e.g., x/4 = 9. Solution: x = 36)
        'division': {
            'problem': "$\\frac{{{1}}}{{{0}}} = {2}$",  # {0}=A, {1}=V, {2}=C
            'answer': "{1} = {3}"  # {1}=V, {3}=X (Solution)
        }
    }

    def __init__(self):
        self._title = "One Step Equations"

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

        # 1. Choose the operation type
        op_type = random.choice(list(self._PROBLEM_TEMPLATES.keys()))
        template = self._PROBLEM_TEMPLATES[op_type]

        # 2. Choose random values
        variable = random.choice(self._VARIABLES)
        # Coefficient/Divisor (A): 2 to 12
        A = random.randint(2, 12)
        # Simple Factor (S_factor): The simple result before multiplying by A (2 to 12)
        S_factor = random.randint(2, 12)

        # Calculate the constant (C) and the final solution (X)
        if op_type == 'multiplication':
            # A * V = C, Solution X = S_factor
            X = S_factor
            C = A * S_factor
        else:  # division
            # V / A = C, Solution X = A * S_factor
            X = A * S_factor
            C = S_factor

        try:
            # Format the problem using A, V, C
            problem_text = f"Solve following expression. \\\\ \\par \\qquad {template['problem'].format(A, variable, C)}"

            # Format the answer using V, X
            answer_text = template['answer'].format(A, variable, C, X)

        except Exception as e:
            print(f"Error generating problem: {e}")
            return None, None

        return problem_text, answer_text

    def get_problem_answer(self) -> tuple[str, str]:
        """Fetches a newly generated problem and logs it."""
        problem_text, answer_text = None, None
        problem_text, answer_text = self.generate_problem()
        # print(f"Problem: {problem_text} | Answer: {answer_text}") # Removed for cleaner output

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
    topic_instance = OneStepEquations()
    topic_instance.title = "One Step Equations"
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()
