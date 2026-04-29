"""Build a first-pass USABO Open Exam calibration bank."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable
import json
import re

import fire
from loguru import logger
import pymupdf


QUESTION_START_RE = re.compile(r"(?m)^\s*(\d{1,2})\.\s*(.*)$")
YEAR_EXAM_RE = re.compile(r"^(20\d{2})_OpenExam\.pdf$")


def extract_year_from_exam_path(path: str | Path) -> int:
    match = YEAR_EXAM_RE.match(Path(path).name)
    if not match:
        raise ValueError(f"Not a canonical Open Exam PDF filename: {path}")
    return int(match.group(1))


def list_exam_pdfs(input_dir: str | Path) -> list[Path]:
    return sorted(Path(input_dir).glob("20??_OpenExam.pdf"))


def read_pdf_pages(pdf_path: str | Path) -> list[tuple[int, str]]:
    document = pymupdf.open(str(pdf_path))
    try:
        return [(index + 1, page.get_text()) for index, page in enumerate(document)]
    finally:
        document.close()


def _page_offsets(pages: list[tuple[int, str]]) -> tuple[str, list[tuple[int, int]]]:
    chunks: list[str] = []
    offsets: list[tuple[int, int]] = []
    position = 0
    for page_number, text in pages:
        offsets.append((position, page_number))
        chunks.append(text)
        position += len(text) + 1
    return "\n".join(chunks), offsets


def _page_for_offset(offset: int, offsets: list[tuple[int, int]]) -> int:
    current_page = offsets[0][1]
    for page_offset, page_number in offsets:
        if page_offset > offset:
            break
        current_page = page_number
    return current_page


def _clean_question_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if stripped.lower().startswith("usabo open exam"):
            continue
        if re.fullmatch(r"page\s+\d+", stripped, flags=re.IGNORECASE):
            continue
        lines.append(stripped)
    return "\n".join(lines).strip()


def extract_question_records_from_text(
    year: int,
    source_pdf: str,
    pages: list[tuple[int, str]],
) -> list[dict[str, object]]:
    text, offsets = _page_offsets(pages)
    candidates = list(QUESTION_START_RE.finditer(text))
    starts = []
    expected = 1

    for match in candidates:
        question_number = int(match.group(1))
        if question_number != expected:
            continue
        starts.append(match)
        expected += 1

    records: list[dict[str, object]] = []
    for index, start in enumerate(starts):
        next_start = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        question_number = int(start.group(1))
        raw_question = text[start.end() : next_start]
        first_line = start.group(2).strip()
        if first_line:
            raw_question = f"{first_line}\n{raw_question}"

        records.append(
            {
                "question_id": f"{year}-{question_number:03d}",
                "year": year,
                "question_number": question_number,
                "answer": "",
                "question_text": _clean_question_text(raw_question),
                "source_pdf": source_pdf,
                "source_page_start": _page_for_offset(start.start(), offsets),
                "source_page_end": _page_for_offset(next_start, offsets),
                "usabo_topic_area": "",
                "campbell_chapter": "",
                "concept": "",
                "subskill": "",
                "reasoning_type": "",
                "difficulty_estimate": "",
                "trap_or_misconception": "",
                "question_type": "",
                "usabo_style_notes": "",
            }
        )
    return records


def extract_question_records_from_pdf(pdf_path: str | Path) -> list[dict[str, object]]:
    year = extract_year_from_exam_path(pdf_path)
    source_pdf = str(pdf_path)
    return extract_question_records_from_text(year, source_pdf, read_pdf_pages(pdf_path))


def write_jsonl(records: Iterable[dict[str, object]], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def write_json(data: object, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _records_by_year(records: Iterable[dict[str, object]]) -> dict[int, list[dict[str, object]]]:
    grouped: dict[int, list[dict[str, object]]] = defaultdict(list)
    for record in records:
        grouped[int(record["year"])].append(record)
    return dict(sorted(grouped.items()))


def write_manual_answer_tasks(
    records: Iterable[dict[str, object]],
    answer_key_paths: dict[int, str],
    path: str | Path,
) -> None:
    grouped = _records_by_year(records)
    lines = [
        "# USABO Open Exam Manual Answer Tasks",
        "",
        "Fill the blank `answer` fields in `data/usabo_calibration/open_exam_questions.jsonl`.",
        "Answer-key PDFs are inconsistent, so this first pass leaves every answer blank for manual review.",
        "",
    ]

    for year, year_records in grouped.items():
        lines.append(f"## {year}")
        lines.append("")
        lines.append(f"- Exam questions: {len(year_records)}")
        lines.append(f"- Answer key source: `{answer_key_paths.get(year, '')}`")
        lines.append("")
        missing = ", ".join(str(record["question_number"]) for record in year_records)
        lines.append(f"Missing answers: {missing}")
        lines.append("")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_wiki(records: Iterable[dict[str, object]], wiki_dir: str | Path) -> None:
    grouped = _records_by_year(records)
    base = Path(wiki_dir)
    years_dir = base / "years"
    years_dir.mkdir(parents=True, exist_ok=True)

    total_questions = sum(len(year_records) for year_records in grouped.values())
    index_lines = [
        "# USABO Calibration Wiki",
        "",
        "This wiki is the LLM-maintained synthesis layer for the USABO Open Exam calibration bank.",
        "Raw PDFs stay in `raw/official_past_exams`; structured question records live in `data/usabo_calibration`.",
        "",
        "## Years",
        "",
    ]
    for year, year_records in grouped.items():
        index_lines.append(f"- [{year}](years/{year}.md): {len(year_records)} extracted questions")
    index_lines.extend(
        [
            "",
            "## Current Scope",
            "",
            f"- Total extracted questions: {total_questions}",
            "- Answers are intentionally blank until manual review.",
            "- Topic, chapter, reasoning, difficulty, and misconception labels are intentionally blank for later calibration work.",
        ]
    )
    (base / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    log_lines = [
        "# USABO Calibration Wiki Log",
        "",
        "## [2026-04-28] ingest | Open Exam skeleton 2003-2018",
        "",
        f"- Extracted {total_questions} question records from canonical Open Exam PDFs.",
        "- Left answer and calibration metadata fields blank for manual review.",
    ]
    (base / "log.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    for year, year_records in grouped.items():
        lines = [
            f"# {year} USABO Open Exam",
            "",
            f"- Extracted questions: {len(year_records)}",
            "- Answer review: pending",
            "- Calibration labels: pending",
            "",
            "## Question Inventory",
            "",
        ]
        for record in year_records:
            lines.append(
                f"- Q{record['question_number']}: `{record['question_id']}` "
                f"page {record['source_page_start']}"
            )
        (years_dir / f"{year}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_calibration_bank(
    input_dir: str | Path = "raw/official_past_exams",
    output_dir: str | Path = "data/usabo_calibration",
    wiki_dir: str | Path = "wiki/usabo_calibration",
) -> dict[str, object]:
    exam_paths = list_exam_pdfs(input_dir)
    records: list[dict[str, object]] = []
    sources = []
    answer_key_paths: dict[int, str] = {}

    for exam_path in exam_paths:
        year = extract_year_from_exam_path(exam_path)
        logger.info("Extracting questions from {}", exam_path)
        year_records = extract_question_records_from_pdf(exam_path)
        records.extend(year_records)

        key_candidates = sorted(Path(input_dir).glob(f"{year}_OpenExam*Key*.pdf"))
        key_path = str(key_candidates[0]) if key_candidates else ""
        answer_key_paths[year] = key_path
        sources.append(
            {
                "year": year,
                "exam_pdf": str(exam_path),
                "answer_key_pdf": key_path,
                "question_count": len(year_records),
            }
        )

    output_base = Path(output_dir)
    questions_path = output_base / "open_exam_questions.jsonl"
    sources_path = output_base / "open_exam_sources.json"
    tasks_path = output_base / "manual_answer_tasks.md"

    write_jsonl(records, questions_path)
    write_json({"sources": sources}, sources_path)
    write_manual_answer_tasks(records, answer_key_paths, tasks_path)
    write_wiki(records, wiki_dir)

    logger.info("Wrote {} question records", len(records))
    return {
        "question_count": len(records),
        "year_count": len(sources),
        "questions_path": str(questions_path),
        "sources_path": str(sources_path),
        "manual_answer_tasks_path": str(tasks_path),
        "wiki_dir": str(wiki_dir),
    }


def main() -> None:
    fire.Fire({"build": build_calibration_bank})


if __name__ == "__main__":
    main()
