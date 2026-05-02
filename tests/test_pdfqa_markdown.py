from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "pdf_to_markdown_qa_tool"))

from pdfqa_md.markdown import build_markdown
from pdfqa_md.models import Answer, Figure, TextLine


def line(text: str, y0: float, x0: float = 0.0, x1: float = 100.0) -> TextLine:
    return TextLine(page_number=1, text=text, bbox=(x0, y0, x1, y0 + 10.0))


def test_build_markdown_cleans_headers_footers_and_reconstructs_obvious_table():
    lines_by_page = {
        1: [
            line("USABO Open Exam", 1),
            line("2005", 2),
            line("8. Scientists have determined that three classes of genes control development.", 10),
            line("shown below, where +++ indicates gene activity.", 20),
            line("Trait Matrix", 30, 0, 100),
            line("Alpha", 40, 120, 150),
            line("Beta", 40, 170, 200),
            line("Gamma", 40, 220, 250),
            line("Delta", 40, 270, 300),
            line("Row A", 50, 0, 60),
            line("+++", 50, 120, 150),
            line("+++", 50, 170, 200),
            line("Row B", 60, 0, 60),
            line("+++", 60, 170, 200),
            line("+++", 60, 220, 250),
            line("Row C", 70, 0, 60),
            line("+++", 70, 220, 250),
            line("+++", 70, 270, 300),
            line("A mutation in Gene C will result in which pattern?", 170),
            line("A. Sepals-Petals-Stamen-Carpels", 180),
            line("B. Sepals-Petals-Petals", 190),
            line("C. Sepals-Petals-Petals-Sepals", 200),
            line("Page 2 of 9", 210),
        ]
    }

    markdown = build_markdown(
        title="Example",
        lines_by_page=lines_by_page,
        figures_by_page={},
        answers={8: Answer(question=8, choice="C", option_text="Sepals-Petals-Petals-Sepals")},
        image_link_root="images",
        include_page_breaks=True,
    )

    assert "<!-- Page" not in markdown
    assert "USABO Open Exam\n2005" not in markdown
    assert "Page 2 of 9" not in markdown
    assert "| Trait Matrix | Alpha | Beta | Gamma | Delta |" in markdown
    assert "| Row B |  | +++ | +++ |  |" in markdown
    assert "# Answer Key" in markdown


def test_build_markdown_keeps_figure_near_question_and_normalizes_roman_list():
    lines_by_page = {
        6: [
            line("24. A red pigment is extracted from a marine alga.", 10),
            line("A. has an absorption spectrum similar to that of chlorophyll", 20),
            line("E. has an absorption spectrum similar to the action spectrum", 30),
            line("25. Given the following pedigree:", 40),
            line("What is (are) the possible mode(s) of inheritance?", 60),
            line("I.", 70),
            line("First mode", 80),
            line("II.", 90),
            line("Second mode", 100),
            line("III.", 110),
            line("Third mode", 120),
            line("Fourth mode", 130),
            line("IV.", 140),
            line("A. II only", 150),
        ]
    }
    figures_by_page = {
        6: [
            Figure(
                page_number=6,
                path=Path("page006_image01.png"),
                bbox=(54.0, 45.0, 360.0, 55.0),
                kind="embedded-image",
            )
        ]
    }

    markdown = build_markdown(
        title="Example",
        lines_by_page=lines_by_page,
        figures_by_page=figures_by_page,
        answers={},
        image_link_root="images",
        include_page_breaks=True,
    )

    question_24 = markdown.split("## Question 24", 1)[1].split("## Question 25", 1)[0]
    question_25 = markdown.split("## Question 25", 1)[1]

    assert "page006_image01.png" not in question_24
    assert "![Figure from page 6](images/page006_image01.png)" in question_25
    assert "- I. First mode" in markdown
    assert "- IV. Fourth mode" in markdown
