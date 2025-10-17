
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: PropertiesOfNumbers
Title: Properties Of Numbers
"""

import os
import random
import sys

from utils import pylatex_pdf as pdf


class PropertiesOfNumbers:
    """A class template for generating and handling math-related problems."""

    def __init__(self):
        self._title = "Properties Of Numbers"
        self._properties = self._load_properties()

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

    def _load_properties(self) -> dict:
        """수의 속성(Property) 목록과 그 정의를 로드합니다."""
        return {
            "Commutative Property of Addition": "The order of addends doesn't change the sum. (a + b = b + a)",
            "Commutative Property of Multiplication": "The order of factors doesn't change the product. (a * b = b * a)",
            "Associative Property of Addition": "The grouping of addends doesn't change the sum. (a + (b + c) = (a + b) + c)",
            "Associative Property of Multiplication": "The grouping of factors doesn't change the product. (a * (b * c) = (a * b) * c)",
            "Distributive Property": "Multiplying a number by a group of numbers added together is the same as doing each multiplication separately. (a * (b + c) = a * b + a * c)",
            "Additive Identity Property": "The sum of any number and zero is that number. (a + 0 = a)",
            "Multiplicative Identity Property": "The product of any number and one is that number. (a * 1 = a)",
            "Additive Inverse Property": "The sum of a number and its opposite (inverse) is zero. (a + (-a) = 0)",
            "Multiplicative Inverse Property": "The product of a number and its reciprocal (inverse) is one. (a * 1/a = 1)",
            "Multiplication Property of Zero": "The product of any number and zero is zero. (a * 0 = 0)",
        }

    def _get_random_values(self, count: int, use_letters: bool = False) -> list[str]:
        """문제에 사용할 무작위 숫자 또는 문자를 생성합니다."""
        if use_letters:
            # a, b, c 등의 문자 사용
            return random.sample(['a', 'b', 'c', 'x', 'y', 'z'], count)
        else:
            # 1~10 사이의 숫자 사용
            return [str(random.randint(1, 10)) for _ in range(count)]

    def _generate_expression(self, property_name: str, values: list[str]) -> str:
        """주어진 속성을 나타내는 수학적 표현식을 생성합니다."""

        v = values  # 값 리스트를 v로 간략화

        if "Commutative Property of Addition" == property_name:
            return f"\\textbf{{Expression: }} ${v[0]} + {v[1]} = {v[1]} + {v[0]}$"

        elif "Commutative Property of Multiplication" == property_name:
            return f"\\textbf{{Expression: }} ${v[0]} \\cdot {v[1]} = {v[1]} \\cdot {v[0]}$"

        elif "Associative Property of Addition" == property_name:
            return f"\\textbf{{Expression: }} $({v[0]} + {v[1]}) + {v[2]} = {v[0]} + ({v[1]} + {v[2]})$"

        elif "Associative Property of Multiplication" == property_name:
            return f"\\textbf{{Expression: }} $({v[0]} \\cdot {v[1]}) \\cdot {v[2]} = {v[0]} \\cdot ({v[1]} \\cdot {v[2]})$"

        elif "Distributive Property" == property_name:
            return f"\\textbf{{Expression: }} ${v[0]} ({v[1]} + {v[2]}) = {v[0]} \\cdot {v[1]} + {v[0]} \\cdot {v[2]}$"

        elif "Additive Identity Property" == property_name:
            return f"\\textbf{{Expression: }} ${v[0]} + 0 = {v[0]}$"

        elif "Multiplicative Identity Property" == property_name:
            return f"\\textbf{{Expression: }} ${v[0]} \\cdot 1 = {v[0]}$"

        elif "Additive Inverse Property" == property_name:
            # a + (-a) = 0. Use (-v0) for negative sign on the second term.
            # If v0 is a letter (e.g., 'x'), it becomes +(-x).
            return f"\\textbf{{Expression: }} ${v[0]} + (-{v[0]}) = 0$"

        elif "Multiplicative Inverse Property" == property_name:
            # a * 1/a = 1. Requires \\frac for the reciprocal.
            # Note: For this property, the generate_problem method should ensure v0 is not '0'.
            return f"\\textbf{{Expression: }} ${v[0]} \\cdot \\frac{{1}}{{{v[0]}}} = 1$"

        elif "Multiplication Property of Zero" == property_name:
            # a * 0 = 0
            return f"\\textbf{{Expression: }} ${v[0]} \\cdot 0 = 0$"

        return "Unknown Property Clue"

    def generate_problem(self) -> tuple[str, str]:
        """
        Generates a single problem and its corresponding answer.
        Returns: (problem_text, answer_text)
        """
        problem_text, answer_text = None, None

        # Implement the problem generation logic here.
        # 1. 무작위 속성 선택
        property_name = random.choice(list(self._properties.keys()))
        property_definition = self._properties[property_name]

        # 2. 값 생성 (문자 또는 숫자 무작위 선택)
        required_values = 3 if any(p in property_name for p in ["Associative", "Distributive"]) else 2

        # 항등원은 1개 값만 필요하지만, 생성 코드를 간단히 하기 위해 2개로 통일
        required_values = max(required_values, 2)

        use_letters = random.random() < 0.5
        values = self._get_random_values(required_values, use_letters)

        # 3. 표현식 생성
        expression_text = self._generate_expression(property_name, values)

        # 4. 문제 텍스트 생성
        problem_text = (
            f"Identify the property of numbers shown in the expression below, and state its rule. \\\\"
            f"\\par \\qquad {expression_text}"
        )

        # 5. 답안 텍스트 생성
        answer_text = (
            f"\\textbf{{Property:}} {property_name} \\\\ \\quad \\textbf{{Rule:}} {property_definition}"
        )

        # \\par\bigskip는 PyLaTeX에서 NoEscape로 처리되어야 합니다.
        problem_text = problem_text.replace(r"\par\bigskip", r"\\ \bigskip")

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
            pdf.generate_pdf_files(f"{self._title} Answers", answer_list, num_column=1)
            print("PDF files successfully generated.")
        except ImportError:
            print("Error: Could not find the 'pdf_handling' module. (Check utils/pdf.py module path)")
        except AttributeError:
            print("Error: 'generate_pdf_files' function is missing in the 'pdf_handling' module.")
        except Exception as e:
            print(f"Error during PDF generation: {e}")


def main():
    topic_instance = PropertiesOfNumbers()
    topic_instance.title = "Properties Of Numbers"
    topic_instance.generate_practice(50)


if __name__ == "__main__":
    main()
