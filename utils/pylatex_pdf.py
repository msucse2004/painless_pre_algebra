import re

from pylatex import Document, Section, Command, NoEscape, Math
from pylatex.base_classes import Environment
import os


# Multicols 환경을 정의하는 클래스 (다중 컬럼 레이아웃을 위해 필요)
class Multicols(Environment):
    """LaTeX의 multicols 환경을 위한 PyLaTeX 클래스."""
    name = 'multicols'

    def __init__(self, cols=1, arguments=None, **kwargs):
        super().__init__(arguments=[cols], **kwargs)


def _create_pylatex_doc(title):
    """PyLaTeX 문서 객체를 생성하고 기본 설정을 추가합니다."""

    #doc = Document(geometry_options=["a4paper", "margin=2cm"])
    doc = Document(geometry_options=["letterpaper", "margin=1cm", "tmargin=2cm", "bmargin=5cm"], page_numbers=True)

    # 필요한 LaTeX 패키지 추가
    #doc.preamble.append(NoEscape(r'\usepackage{amsmath}'))
    #doc.preamble.append(NoEscape(r'\usepackage{amssymb}'))
    #doc.preamble.append(NoEscape(r'\usepackage{multicol}'))  # 다중 컬럼용
    # 필수 패키지
    doc.preamble.append(NoEscape(r'\usepackage{amsmath, amssymb, multicol}'))
    doc.preamble.append(NoEscape(r'\setlength{\columnseprule}{0.1pt}'))


    # 0.4pt는 선의 기본 두께입니다. 선을 없애려면 0pt로 설정하면 됩니다.
    doc.preamble.append(NoEscape(r'\setlength{\columnseprule}{0.1pt}'))


    # 제목 설정
    doc.preamble.append(Command('title', NoEscape(r'\textbf{\LARGE ' + title.replace('_', r'\_') + r'}')))
    doc.preamble.append(NoEscape(r'\date{}'))
    doc.preamble.append(NoEscape(r'\author{Underline and Circle where necessary!!}'))

    return doc


def generate_pdf_files(
        project: str,
        content_list: list[str],
        num_column: int = 1,
        row_spacing: int = 20  # PyLaTeX에서는 row_spacing을 직접 적용하지 않습니다.
):

    doc = _create_pylatex_doc(project)
    doc.append(NoEscape(r'\maketitle'))
    # \maketitle 이후의 불필요한 여백을 상쇄하기 위해 음수 공간을 삽입합니다.
    doc.append(NoEscape(r'\vspace*{-0.5cm}'))


    is_problem_sheet = "Problem" in project

    # === 콘텐츠 추가 ===
    # 별도의 Section 없이 바로 문제 목록을 시작하여 워크시트 느낌을 살림

    if num_column > 1:
        # 이렇게 하면 항목 간의 VSPACE가 균일하게 유지됩니다.
        doc.append(NoEscape(r'\raggedcolumns'))

        # \begin{multicols}{N} ... \end{multicols} 환경을 전체 문제 목록에 적용
        with doc.create(Multicols(cols=num_column)):
            _add_content_to_pylatex(doc, content_list, is_problem_sheet, row_spacing)
    else:
        _add_content_to_pylatex(doc, content_list, is_problem_sheet, row_spacing)

    # === PDF 생성 ===
    try:
        filename = project.replace(" ", "_")

        # 컴파일러 호출
        doc.generate_pdf(filename, clean_tex=True, compiler='pdflatex', silent=False)
        print(f"***'{filename}.pdf' 파일이 PyLaTeX로 성공적으로 생성되었습니다.")

    except Exception as e:
        print(f"\n❌ PyLaTeX 컴파일 중 오류 발생: {e}")
        print(f"   -> 다음을 확인하세요:")
        print(f"      1. 시스템에 'pdflatex'가 설치되어 있고 PATH에 등록되었는지 확인하세요.")
        print(f"      2. {filename}.log 파일을 열어 컴파일 오류 내용을 확인하세요.\n")


def _add_content_to_pylatex(doc, content_list, is_problem_sheet, row_spacing=1):
    """목록 항목을 PyLaTeX 문서에 추가합니다."""

    spacing_length = f'{row_spacing / 10:.1f}mm'

    # $...$, $$...$$, \[...\], \begin...\end... 정규식
    pattern = re.compile(
        r"(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\begin\{.*?\}.*?\\end\{.*?\})",
        re.DOTALL
    )

    safe_commands = [r'\quad', r'\qquad', r'\\', r'\centerline', r'\mbox']

    for i, content in enumerate(content_list):
        doc.append(NoEscape(r'\Large'))
        # 1. 문제/정답 번호 추가 (ex: 1.)
        doc.append(f'{i + 1}. ')

        # 2. LaTeX 수식 부분 처리
        #text_parts = content.split('$')
        parts = pattern.split(content)

        for part in parts:
            if not part.strip():
                continue

            # --- 수식 또는 환경 구분 ---
            if part.startswith('$$') and part.endswith('$$'):
                expr = part[2:-2].strip()
                with doc.create(Math(inline=False)) as math:
                    math.append(NoEscape(expr))

            elif part.startswith('$') and part.endswith('$'):
                expr = part[1:-1].strip()
                with doc.create(Math(inline=True)) as math:
                    math.append(NoEscape(expr))

            elif part.startswith(r'\[') and part.endswith(r'\]'):
                expr = part[2:-2].strip()
                with doc.create(Math(inline=False)) as math:
                    math.append(NoEscape(expr))

            elif part.strip().startswith(r'\begin') and r'\end' in part:
                if re.search(r'\\(frac|sqrt|sum|int|pi|theta|alpha|beta|sin|cos|tan|log|ln)', part):
                    safe_part = re.sub(
                        r'(\\begin\{[a-zA-Z*]+\})(.*?)(\\end\{[a-zA-Z*]+\})',
                        lambda m: m.group(1)
                                  + f'$$ {m.group(2).strip()} $$'
                                  + m.group(3),
                        part,
                        flags=re.DOTALL
                    )
                    doc.append(NoEscape(safe_part))
                else:
                    doc.append(NoEscape(part))

            # --- 수식 명령 자동 감지 ---
            elif re.search(r'\\(frac|sqrt|sum|int|pi|theta|alpha|beta|sin|cos|tan|log|ln)', part):
                with doc.create(Math(inline=True)) as math:
                    math.append(NoEscape(part.strip()))

            else:
                #doc.append(part.strip())
                is_latex_command = any(part.strip().startswith(cmd) for cmd in safe_commands)

                if r'\\' in part or is_latex_command:
                    doc.append(NoEscape(part.strip()))  # \quad, \qquad 포함
                else:
                    doc.append(part.strip())


        # 'Problems'의 경우 공백이 필요하고, 'Answers'의 경우 공백이 적어도 됨
        if is_problem_sheet:
             # 문제지에는 풀이 공간을 위해 넉넉한 세로 공백을 추가
             doc.append(NoEscape(r'\par\vspace{' + spacing_length + r'}\par\nobreak'))

        else:
             # 정답지는 간결하게 작은 공백만 추가
            doc.append(NoEscape(r'\par\medskip'))


    # === 페이지 하단 공간 확보 ===
    doc.append(NoEscape(r'\vfill\null'))


def main():
    numerator, denominator = 2, 3
    content_list = [
        "Simplify \\frac{2}{3} + \\frac{1}{6}",
        "Find \\sqrt{9}",
        "Convert \\frac{3}{4} to decimal form.",
        "Compute $\\frac{1}{2} + \\frac{1}{3}$",  # 이미 $로 감싼 것은 그대로 처리
        "quotation text example \\begin{quotation} \\frac{1}{2} \\end{quotation}",
        "\\quad inline",
        "\\qquad inline2",
        f"\\qquad Simplify fractions: \\par \\qquad $\\frac{{{numerator}}}{{{denominator}}}$"
    ]
    generate_pdf_files(f"test_pylatext_format", content_list, num_column=1, row_spacing=40)



if __name__ == "__main__":
    main()