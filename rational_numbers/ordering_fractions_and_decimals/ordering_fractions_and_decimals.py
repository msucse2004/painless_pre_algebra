
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: OrderingFractionsAndDecimals
Title: Ordering Fractions And Decimals
"""

import os
import random
import sys


from utils import pylatex_pdf as pdf
from utils.fractions import to_latex_friction


class OrderingFractionsAndDecimals:
    """A class template for generating and handling math-related problems."""

    def __init__(self):
        self._title = "Ordering Fractions And Decimals"

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

    def make_comparison_problem(self) -> tuple[str, str]:
        problem_text, answer_text = None, None

        numerator1 = random.randint(1, 20)
        denominator1 = random.randint(2, 20)
        decimal1 = numerator1 / denominator1
        formatted_decimal1 = f"{decimal1:.2f}"

        numerator2 = random.randint(1, 20)
        denominator2 = random.randint(2, 20)
        decimal2 = numerator2 / denominator2
        formatted_decimal2 = f"{decimal2:.2f}"

        term1 = to_latex_friction(numerator1, denominator1)
        term2 = random.choice([formatted_decimal2, to_latex_friction(numerator2, denominator2)])

        problem_text = f"Compare. User >, < or =. \\\\ \\par \\qquad \\qquad {term1} ___ {term2}"
        if decimal1 > decimal2:
            answer_text = f"{term1}  > {term2}"
        elif decimal1 < decimal2:
            answer_text = f"{term1}  < {term2}"
        else:
            answer_text = f"{term1}  = {term2}"

        # Implement the problem generation logic here.

        return problem_text, answer_text

    def make_ordering_problem(self) -> tuple[str, str]:
        # 사용할 상수 정의
        number_of_generation = 4  # 생성할 숫자의 개수

        # 0.5 미만이면 오름차순(ascending), 0.5 이상이면 내림차순(descending)
        is_ascending = random.random() < 0.5
        order_type = "ascending" if is_ascending else "descending"

        # 문제에 사용될 숫자 데이터를 저장할 목록
        # data_objects: 원본 문자열, float 값, 타입(fraction/decimal)을 저장
        data_objects = []

        # 1. 데이터 생성
        for _ in range(number_of_generation):
            # 분수 또는 소수 중 무작위 선택
            is_fraction = random.random() < 0.5

            if is_fraction:
                # 간단한 분수 생성 (예: 1/4, 2/5)
                n = random.randint(1, 9)
                d = random.choice([2, 3, 4, 5, 8, 10])
                # 분수 문자열과 십진수 값
                original_str = f"\\frac{{{n}}}{{{d}}}"  # LaTeX 분수 형식
                float_value = n / d
            else:
                # 간단한 소수 생성 (예: 0.25, 1.5)
                integer_part = random.randint(0, 2)
                decimal_part = random.randint(10, 99) / 100
                float_value = integer_part + decimal_part
                # 소수 문자열
                original_str = f"{float_value:.2f}"

            data_objects.append({
                "original_str": original_str,
                "float_value": float_value
            })

        # 2. 문제 문자열 생성
        # LaTeX 환경에서는 모든 숫자를 수학 모드로 감싸야 합니다.
        # 문제에 제시될 숫자들을 랜덤하게 섞어줍니다.
        random.shuffle(data_objects)

        problem_numbers = [f"${d['original_str']}$" for d in data_objects]
        problem_text = (f"list following rational numbers to {order_type} orders: \\\\ \\par \\qquad \\qquad"
                        f"[{', '.join(problem_numbers)}]"
                        )

        # 3. 정렬 및 답안 문자열 생성
        # float_value를 기준으로 정렬합니다. (is_ascending이 True면 오름차순)
        sorted_objects = sorted(
            data_objects,
            key=lambda x: x['float_value'],
            reverse=not is_ascending  # 오름차순(is_ascending=True)이면 reverse=False
        )

        # 정렬된 순서대로 답안 문자열을 생성합니다.
        answer_numbers = [f"${d['original_str']}$" for d in sorted_objects]
        answer_text = " < ".join(answer_numbers) if is_ascending else " > ".join(answer_numbers)

        return problem_text, answer_text

    def generate_problem(self) -> tuple[str, str]:
        """
        Generates a single problem and its corresponding answer.
        Returns: (problem_text, answer_text)
        """
        problem_text, answer_text = None, None

        # Implement the problem generation logic here.

        problem_pool = []
        answer_pool = []

        #problem, answer = self.make_comparison_problem()
        #problem_pool.append(problem)
        #answer_pool.append(answer)

        problem, answer = self.make_ordering_problem()
        problem_pool.append(problem)
        answer_pool.append(answer)

        problem_text = random.choice(problem_pool)
        index = problem_text.index(problem_text)
        answer_text = answer_pool[index]

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
    topic_instance = OrderingFractionsAndDecimals()
    topic_instance.title = "Ordering Fractions And Decimals"
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()
