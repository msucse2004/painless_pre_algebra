import os
import random
import sys

# Assuming 'utils' and 'pylatex_pdf' are correctly configured in the user's environment
from utils import pylatex_pdf as pdf


class RatioRateUnitRate:
    """A class template for generating and handling math-related problems."""

    # 문제 생성을 위한 기본 데이터 리스트
    _UNITS_A = ['miles', 'dollars', 'books', 'pages', 'steps', 'cookies', 'widgets']
    _UNITS_B = ['hours', 'days', 'minutes', 'trips', 'boxes', 'weeks']
    _NOUNS_A = ['boys', 'girls', 'cats', 'dogs', 'red cars', 'blue cars', 'pencils', 'erasers']
    _NOUNS_B = ['teachers', 'students', 'people', 'workers', 'chefs']
    _VERBS = ['drove', 'read', 'walked', 'baked', 'produced', 'spent']

    # 문제 템플릿: (정답 분류, 문제 템플릿 문자열)
    _TEMPLATES = {
        # 같은 종류의 두 양을 비교 (예: 소년 15명 대 소녀 12명)
        'Ratio': [
            ("Ratio", "{0} {noun_a} to {1} {noun_b}"),
            ("Ratio", "The ratio of {0} {noun_a} to {1} {noun_b}"),
            ("Ratio", "{0} out of {1} {noun_a} are {noun_b}"),
        ],
        # 다른 종류의 두 양을 비교 (예: 12명의 학생이 60달러를 사용)
        'Rate': [
            ("Rate", "{0} {noun_b} {verb} {1} {unit_a}"),
            ("Rate", "{0} {unit_a} in {1} {unit_b}"),
            ("Rate", "The cost is \\${0} for {1} {unit_b} of usage"),
        ],
        # 두 번째 양이 1단위인 비 (예: 시간당 30달러)
        'Unit Rate': [
            ("Unit Rate", "A {noun_b_singular} charges \\${0} per hour"),
            ("Unit Rate", "{0} {unit_a} per minute"),
            ("Unit Rate", "{0} {unit_a} for every box"),
            ("Unit Rate", "A car travels {0} miles per gallon"),
        ]
    }

    def __init__(self):
        self._title = "Ratio Rate Unit Rate"

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

        # 1. 유형 선택 (Ratio, Rate, Unit Rate)
        type_choice = random.choice(list(self._TEMPLATES.keys()))

        # 2. 템플릿 및 정답 선택
        answer, template = random.choice(self._TEMPLATES[type_choice])

        # 3. 무작위 숫자 생성
        num1 = random.randint(3, 30)
        num2 = random.randint(3, 30)

        # 4. 문맥에 맞는 단어 선택 및 포맷팅 준비
        context = {}
        if type_choice == 'Ratio':
            context['noun_a'] = random.choice(self._NOUNS_A)
            # noun_a와 다른 noun_b를 선택
            context['noun_b'] = random.choice([n for n in self._NOUNS_A if n != context['noun_a']])
        elif type_choice == 'Rate':
            context['noun_b'] = random.choice(self._NOUNS_B)
            context['verb'] = random.choice(self._VERBS)
            context['unit_a'] = random.choice(self._UNITS_A)
            context['unit_b'] = random.choice(self._UNITS_B)
        elif type_choice == 'Unit Rate':
            context['noun_b_singular'] = random.choice(self._NOUNS_B)[
                :-1]  # 복수형에서 단수형으로 변환 (예: 'teachers' -> 'teacher')
            context['unit_a'] = random.choice(self._UNITS_A)
            context['unit_b'] = random.choice(self._UNITS_B)

        # 5. 문제 문자열 포맷팅 및 정답 설정
        try:
            problem_description = template.format(num1, num2, **context)

            # 최종 문제 형식: "이것이 Ratio, Rate, Unit Rate 중 무엇인지 결정하십시오: [문제 내용]"
            problem_text = f"Decide whether this is a ratio, rate, or unit rate: \\\\ \\par \\qquad {problem_description}"
            answer_text = answer

        except Exception as e:
            print(f"Formatting error: {e}")
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
            # 문제를 1열, 정답을 4열로 PDF 생성
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
    topic_instance = RatioRateUnitRate()
    topic_instance.title = "Ratio Rate Unit Rate"
    topic_instance.generate_practice(5)


if __name__ == "__main__":
    main()
