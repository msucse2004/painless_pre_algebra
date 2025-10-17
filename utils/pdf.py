import os
from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos
import matplotlib.pyplot as plt
from io import BytesIO

# Set up font paths (assumed to be correct)
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
FONT_FILE_NORMAL = os.path.join(FONT_DIR, 'STIXTwoMath-Regular.ttf')
FONT_FILE_BOLD = os.path.join(FONT_DIR, 'STIXTwoMath-Regular.ttf')
FONT_FAMILY = "STIXTwoText-Regular"
LINE_SPACE_AFTER_TITLE = 15

def generate_pdf_files(
        project,
        problem_answer_list,
        num_column=1,
        row_spacing=20
):

    try:

        # Generate Problems PDF
        pdf_problems = _create_pdf(f"{project}")
        _add_content(
            pdf_problems,
            problem_answer_list,
            num_column,
            row_spacing,
            project
        )
        pdf_problems.output(f"{project.replace(" ", "_")}.pdf")
        print(f"***'{project.replace(" ", "_")}.pdf' has been created.")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def _create_pdf(title):
    """Helper to create a new FPDF object with standard settings."""
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    if not os.path.exists(FONT_FILE_NORMAL) or not os.path.exists(FONT_FILE_BOLD):
        raise FileNotFoundError(f"One or more font files not found in {FONT_DIR}")
    pdf.add_font(FONT_FAMILY, "", FONT_FILE_NORMAL)
    pdf.add_font(FONT_FAMILY, "B", FONT_FILE_BOLD)
    pdf.set_font(FONT_FAMILY, 'B', 16)
    pdf.cell(w=0, h=10, text=title, new_x=XPos.LMARGIN, new_y=YPos.TOP, align=Align.C)
    pdf.ln(LINE_SPACE_AFTER_TITLE)
    pdf.set_font(FONT_FAMILY, '', 14)
    return pdf

def _render_latex_to_image(latex_string: str) -> BytesIO:
    """
    LaTeX 수식 문자열을 Matplotlib을 사용하여 PNG 형식의 BytesIO 객체로 렌더링합니다.
    (fpdf2는 PNG/JPG 파일을 직접 삽입할 수 있습니다.)
    """
    # Matplotlib의 LaTeX 렌더링 기능(mathtext)을 사용합니다.
    # r'$...$' 형식으로 LaTeX 수식을 감싸야 합니다.
    text = r'$' + latex_string + r'$'

    # 임시 Figure 및 Axes 생성
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0.0)  # 배경 투명하게 설정

    # 텍스트 객체 생성 (수식 렌더링)
    plt.text(0.0, 0.0, text, fontsize=14, color='black',
             verticalalignment='bottom', horizontalalignment='left')

    # 축 숨기기
    plt.gca().axis('off')

    # 그림 경계에 맞게 Figure 크기 자동 조정
    plt.tight_layout(pad=0)

    # BytesIO 객체에 PNG 형식으로 저장 (파일 시스템에 저장하지 않음)
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)  # Figure 닫기

    img_buffer.seek(0)
    return img_buffer


def _add_content(pdf, content_list, num_columns, row_spacing, project_title=None):
    """
    내용을 다중 열에 추가하고, LaTeX 수식 부분을 감지하여 이미지로 대체하며,
    컬럼 너비를 초과하는 텍스트는 자동으로 줄 바꿈합니다.
    """
    margin = 10
    total_width = pdf.w - 2 * margin
    col_width = total_width / num_columns
    column_y = [pdf.get_y()] * num_columns

    line_height = pdf.font_size * 1.2

    # 텍스트와 이미지 사이에 약간의 공간 추가
    INTER_PART_SPACING = 1.5

    START_DELIMITER = "$"
    END_DELIMITER = "$"

    for i, content in enumerate(content_list):
        col_index = i % num_columns

        # 1. 문제 시작 위치 설정
        pdf.set_xy(margin + col_index * col_width, column_y[col_index])

        # 2. 문제 번호 출력 (Multi-cell 대신 Cell 사용, 번호가 한 줄을 넘지 않기 때문)
        problem_number = f"{i + 1}) "
        # 문제 번호 출력 시 W=col_width/4 정도의 작은 값으로 설정하고 Y는 그대로 둠
        pdf.cell(w=pdf.get_string_width(problem_number) + 1, h=line_height, text=problem_number, new_x=XPos.RIGHT,
                 new_y=YPos.CURRENT)

        # 번호 출력 후 커서 위치 업데이트
        current_x = pdf.get_x()
        current_y = pdf.get_y()

        # 문제 번호를 제외한 실제 콘텐츠
        content_text = content.strip()
        parts = content_text.split(START_DELIMITER)

        local_max_y_in_cell = current_y

        # 첫 파트의 시작 Y 좌표를 저장 (텍스트 한 줄일 때 Y 보정을 위해)
        start_y_for_part = current_y

        for j, part in enumerate(parts):

            # 매 파트 시작 시, pdf 커서 위치를 current_x, current_y로 정확히 설정
            pdf.set_xy(current_x, current_y)

            is_latex_part = (j % 2 != 0) and (j != 0)  # 수식 파트인지 확인

            # 현재 X 위치부터 컬럼 끝까지의 남은 너비
            remaining_width = (margin + (col_index + 1) * col_width) - current_x

            # 이미지 높이 추정
            img_height = line_height * 1.5

            if is_latex_part:
                # 3. LaTeX 수식 처리
                latex_part = part
                try:
                    processed_latex = latex_part.replace("\\\\", "\\")
                    img_buffer = _render_latex_to_image(processed_latex)
                except Exception as e:
                    print(f"Error rendering LaTeX '{latex_part}': {e}")
                    # 렌더링 실패 시, 일반 텍스트로 multi_cell 처리
                    pdf.multi_cell(
                        w=remaining_width,
                        h=line_height,
                        text=f"${latex_part}$",
                        align=Align.L,
                        border=0,
                        new_x=XPos.LMARGIN,
                        new_y=YPos.TOP
                    )
                    # multi_cell 후 Y 좌표 및 X 좌표 업데이트
                    current_y = pdf.get_y()
                    current_x = margin + col_index * col_width
                    local_max_y_in_cell = max(local_max_y_in_cell, current_y)
                    continue

                # 이미지 너비 추정 (줄 바꿈 판단 및 X 이동에 사용)
                estimated_img_width = pdf.get_string_width(processed_latex) * 1.5 + 5

                # --- 이미지 줄 바꿈 로직 ---
                if estimated_img_width + INTER_PART_SPACING > remaining_width:
                    current_y += img_height
                    current_x = margin + col_index * col_width
                    pdf.set_xy(current_x, current_y)
                # --- 이미지 줄 바꿈 로직 끝 ---

                # 이미지 삽입
                pdf.image(img_buffer, x=current_x, y=current_y, h=img_height, type='PNG')

                current_x += estimated_img_width + INTER_PART_SPACING

                image_bottom_y = current_y + img_height
                local_max_y_in_cell = max(local_max_y_in_cell, image_bottom_y)

                # 이미지 다음은 항상 새 줄에서 시작하도록 강제하는 것이 Answer의 짧은 수식에 유리
                current_y = image_bottom_y
                current_x = margin + col_index * col_width

            else:
                # 4. 일반 텍스트 처리
                # multi_cell은 현재 X 위치부터 남은 컬럼 너비만큼 사용하고 자동으로 줄 바꿈
                remaining_width_in_col = (margin + (col_index + 1) * col_width) - current_x

                y_before_cell = pdf.get_y()

                pdf.multi_cell(
                    w=remaining_width_in_col,
                    h=line_height,
                    text=part,
                    align=Align.L,
                    border=0,
                    new_x=XPos.LMARGIN,
                    new_y=YPos.TOP
                )

                # multi_cell 후 Y 위치 업데이트 및 local_max_y_in_cell 업데이트
                y_after_cell = pdf.get_y()

                # --- 핵심 수정: 텍스트가 한 줄만 차지했을 경우, Y 좌표를 현재 라인으로 유지 ---
                # multi_cell이 Y를 다음 줄 시작점으로 옮겼지만, 텍스트 길이가 짧아 현재 라인에
                # 다음 파트를 이어서 출력해야 할 경우, Y를 보정해야 함.
                # 그러나 multi_cell의 new_x=XPos.LMARGIN 속성 때문에 다음 텍스트는 항상 컬럼 시작점.

                # 텍스트가 실제로 줄바꿈 없이 한 줄로 끝났을 때만 current_y를 보정합니다.
                if abs(y_after_cell - y_before_cell) < line_height * 0.1 and j == len(parts) - 1:
                    # 텍스트가 한 줄이고 마지막 파트일 때, local_max_y_in_cell을 현재 줄 높이로 유지
                    current_y = y_before_cell + line_height
                else:
                    current_y = y_after_cell

                local_max_y_in_cell = max(local_max_y_in_cell, current_y)
                current_x = margin + col_index * col_width

        # 5. 다음 문제 시작점 설정
        # Answer의 경우 수식 이미지가 한 줄에 다 들어갈 가능성이 높음
        column_y[col_index] = local_max_y_in_cell + row_spacing

        # 6. 페이지 나누기 검사
        if max(column_y) > pdf.page_break_trigger - 20 and (i + 1) % num_columns == 0:
            pdf.add_page()
            if project_title:
                pdf.set_font(FONT_FAMILY, 'B', 16)
                pdf.cell(w=0, h=10, text=project_title, new_x=XPos.LMARGIN, new_y=YPos.TOP, align=Align.C)
                pdf.ln(LINE_SPACE_AFTER_TITLE)
            pdf.set_font(FONT_FAMILY, '', 14)
            current_pdf_y = pdf.get_y()
            column_y = [current_pdf_y] * num_columns
