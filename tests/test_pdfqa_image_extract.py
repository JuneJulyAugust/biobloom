from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "pdf_to_markdown_qa_tool"))

from pdfqa_md.image_extract import _remove_duplicate_vector_crops
from pdfqa_md.models import Figure


def test_remove_duplicate_vector_crops_keeps_embedded_image_over_matching_crop():
    embedded = Figure(
        page_number=6,
        path=Path("images/page006_image01.png"),
        bbox=(54.0, 365.0, 360.0, 450.5),
        kind="embedded-image",
    )
    duplicate_crop = Figure(
        page_number=6,
        path=Path("images/page006_figure01.png"),
        bbox=(54.0, 365.0, 360.0, 450.5),
        kind="vector-crop",
    )
    distinct_crop = Figure(
        page_number=6,
        path=Path("images/page006_figure02.png"),
        bbox=(420.0, 365.0, 520.0, 450.5),
        kind="vector-crop",
    )

    figures = _remove_duplicate_vector_crops([embedded, duplicate_crop, distinct_crop])

    assert figures == [embedded, distinct_crop]
