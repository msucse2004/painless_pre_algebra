
"""
$NAME.py
--------------------
Auto-generated class template for math problem generation and PDF export.

Class: WritingExpressions
Title: Writing Expressions
"""

import os
import random
import sys

from utils import pylatex_pdf as pdf


class WritingExpressions:
    """A class template for generating and handling math-related problems."""
    # 연산자별 키워드 목록
    _KEYWORDS = {
        '+': ["sum of {0} and {1}", "{0} added to {1}", "{0} plus {1}", "{0} increased by {1}", "{0} exceeds {1}",
              "{0} in all", "total of {0} and {1}"],
        '-': ["difference of {0} and {1}", "{0} minus {1}", "{0} decreased by {1}"],
        # 뺄셈 순서 반전 키워드 (Op2 - Op1)
        '-_rev': ["{1} less than {0}", "{1} subtracted from {0}", "{1} reduced by {0}"],
        '*': ["product of {0} and {1}", "{0} times {1}"],
        '*_mult': ["twice {0}", "triple {0}", "double {0}"],  # 단일 피연산자에 대한 곱셈
        '/': ["quotient of {0} and {1}", "ratio of {0} and {1}", "{0} divided by {1}"],
        '^': ["{0} squared", "{0} cubed", "{0} raised to the power of {1}"],
    }
    # 문제에 사용할 변수와 숫자
    _VARIABLES = ['x', 'y', 'a', 'b', 'c', 'n', 'q', 'u', 'e', 'm']
    _NUMBERS = list(range(2, 11))  # 2부터 10까지의 숫자

    def __init__(self):
        self._title = "Writing Expressions"

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

    def _get_random_terms(self, count: int, allow_variables: bool = True, allow_numbers: bool = True) -> list:
        """문제에 사용할 무작위 숫자 또는 변수를 생성합니다."""
        terms = []
        for _ in range(count):
            choice = random.choice([0, 1])  # 0: 숫자, 1: 변수

            if allow_variables and (choice == 1 or not allow_numbers):
                # 변수 사용
                terms.append(random.choice(self._VARIABLES))
            elif allow_numbers:
                # 숫자 사용
                terms.append(random.choice(self._NUMBERS))
            else:
                # 폴백: 이 상황은 발생하지 않아야 함
                terms.append('z')
        return terms

    def generate_problem(self) -> tuple[str, str]:
        """
                Generates a single problem and its corresponding answer.
                Returns: (problem_text, answer_text)
                """
        # 1. 무작위 연산 선택
        operator_key = random.choice(list(self._KEYWORDS.keys()))

        problem_text, answer_text = "", ""

        if operator_key == '*':
            # 50% 확률로 단항 곱셈 (twice, triple) 사용
            if random.random() < 0.5:
                operator_key = '*_mult'

        # 2. 항(Term) 생성
        if operator_key in ['*_mult', '^']:
            # 단일 항 또는 두 항이 필요합니다.
            if operator_key == '^':
                # 지수 문제: Base(변수/숫자)와 Exponent(숫자 2, 3, 4)가 필요합니다.
                base = self._get_random_terms(1, allow_numbers=True)[0]
                exponent = random.choice([2, 3, 4])
                terms = [base, exponent]
            else:  # *_mult (twice, triple)
                terms = self._get_random_terms(1, allow_variables=True)

        elif operator_key in ['+', '-', '-_rev', '*', '/']:
            # 이항 연산: 두 항이 필요합니다.
            terms = self._get_random_terms(2, allow_variables=True)
            # 덧셈, 곱셈은 순서가 바뀌어도 상관없지만, 뺄셈/나눗셈은 순서를 다르게 생성하여 복잡성을 높입니다.
            # 중복 방지를 위해 terms가 (5, 5)와 같이 같은 값인 경우 다시 생성할 수 있으나, 일단 건너뜁니다.

            # 숫자와 변수가 섞여 있을 경우, 보통 숫자가 먼저 오는 것이 자연스러움 (예: 5 + x)
            if all(isinstance(t, str) and not t.isdigit() for t in terms):
                # 둘 다 변수일 경우
                pass
            elif all(isinstance(t, int) for t in terms):
                # 둘 다 숫자일 경우
                pass
            else:
                # 숫자와 변수가 섞여 있을 경우: 덧셈, 곱셈은 숫자를 Op1로 선호
                if operator_key in ['+', '*']:
                    # 만약 terms[0]이 변수이고 terms[1]이 숫자라면, 순서를 바꿉니다.
                    if isinstance(terms[0], str) and isinstance(terms[1], int):
                        terms.reverse()
                # 뺄셈, 나눗셈은 순서를 바꾸지 않아야 합니다.

        # 3. 문제 텍스트 생성
        keyword_template = random.choice(self._KEYWORDS[operator_key])

        # 항을 문자열로 변환
        str_terms = [str(t) for t in terms]

        try:
            problem_text = f"Write an algebraic expression for: \\\\ \\par \\qquad {keyword_template.format(*str_terms)}"
        except IndexError:
            # 항의 개수가 맞지 않는 오류 방지
            return None, None

        # 4. 정답 텍스트 생성
        t1, t2 = str_terms[0], str_terms[1] if len(str_terms) > 1 else None

        if operator_key == '+':
            answer_text = f"{t1}+{t2}"

        elif operator_key == '-':
            # 차이 (Op1 - Op2)
            answer_text = f"{t1}-{t2}"

        elif operator_key == '-_rev':
            # Less than / Subtracted from (Op2 - Op1)
            answer_text = f"{t1}-{t2}"  # keyword_template.format(*str_terms) 에서 t1이 Op2 위치, t2가 Op1 위치

            # t1, t2가 포매팅 템플릿에 들어갈 때의 위치(Op1, Op2)가 반전되어야 합니다.
            # 예시: "{1} less than {0}" -> format(7, e) -> "e less than 7"
            # 정답은 7-e 입니다. (t1은 7, t2는 e)
            answer_text = f"{t1}-{t2}"  # 템플릿에 들어간 순서대로 t1(Op2), t2(Op1)이 결정되었으므로 템플릿 순서대로 작성합니다.
            # NOTE: 키워드 정의와 템플릿 포매팅 순서에 따라 달라집니다.
            # 현재 키워드는 "{1} less than {0}" 입니다.
            # terms = [Op1, Op2]
            # problem_text = "{1} less than {0}".format(t1, t2) -> "{t2} less than {t1}"
            # 정답: t1 - t2

            # 템플릿에 들어간 항의 순서를 다시 확인합니다.
            # keyword_template.format(t1, t2) 에서 t1, t2는 terms[0], terms[1] 입니다.
            # Example: terms=['7', 'e']
            # template: "{1} less than {0}"
            # problem: "e less than 7"
            # answer: 7-e (즉, t1-t2) -> 현재 로직은 문제없음
            answer_text = f"{t1}-{t2}"  # Op1(7) - Op2(e)

        elif operator_key == '*':
            # Product of 6 and q -> 6q (숫자가 앞에 오도록 함)
            # 두 항 중 하나라도 변수이면 곱셈 기호 생략, 아니면 기호 포함
            if not t1.isalpha() and not t2.isalpha():  # 둘 다 숫자
                answer_text = f"{t1} \\times {t2}"  # LaTeX에서 곱셈 기호(\times) 사용
            else:
                # 숫자와 변수가 섞여 있으면 숫자가 앞에 오게 정렬
                if t1.isdigit() and t2.isalpha():
                    answer_text = f"{t1}{t2}"
                elif t1.isalpha() and t2.isdigit():
                    answer_text = f"{t2}{t1}"
                else:  # 둘 다 변수
                    answer_text = f"{t1}{t2}"

        elif operator_key == '*_mult':
            # twice x -> 2x, triple x -> 3x
            if "twice" in problem_text:
                answer_text = f"2 \\cdot {t1}"
            elif "triple" in problem_text:
                answer_text = f"3 \\cdot {t1}"
            elif "double" in problem_text:
                answer_text = f"2 \\cdot {t1}"
            else:
                # 일반 곱셈으로 폴백
                answer_text = f"\\text{Error: Unknown multiplier}"

        elif operator_key == '/':
            # Quotient of c and 7 -> c/7 (분수 형태로 정답 표시)
            answer_text = f"\\frac{{{t1}}}{{{t2}}}"

        elif operator_key == '^':
            base = str_terms[0]
            exp = str_terms[1]

            if "squared" in problem_text:
                answer_text = f"{base}^{{2}}"
            elif "cubed" in problem_text:
                answer_text = f"{base}^{{3}}"
            else:  # raised to the power of {1}
                answer_text = f"{base}^{{{exp}}}"

        # LaTeX 수식 모드 적용
        if answer_text and not answer_text.startswith("\\text"):
            answer_text = f"${answer_text}$"

        # 문제 텍스트의 첫 글자를 대문자로
        problem_text = problem_text[0].upper() + problem_text[1:]

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
    topic_instance = WritingExpressions()
    topic_instance.title = "Writing Expressions"
    topic_instance.generate_practice(100)


if __name__ == "__main__":
    main()
