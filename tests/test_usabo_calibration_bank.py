import json

from biobloom.usabo_calibration_bank import extract_question_records_from_text
from biobloom.usabo_calibration_bank import write_audit_files
from biobloom.usabo_calibration_bank import write_jsonl


def test_extract_question_records_from_text_uses_sequential_question_starts():
    pages = [
        (
            1,
            """USABO Open Exam
Questions 1 and 2. Please use the following options.
1. First question text.
A. Alpha
B. Beta
2. Second question text.
A. Gamma
B. Delta
Choice
1. This table row should not become question three.
3. Third question text.
A. One
B. Two
""",
        )
    ]

    records = extract_question_records_from_text(2018, "raw/2018_OpenExam.pdf", pages)

    assert [record["question_number"] for record in records] == [1, 2, 3]
    assert records[0]["question_id"] == "2018-001"
    assert records[0]["answer"] == ""
    assert records[0]["source_page_start"] == 1
    assert records[2]["question_text"].startswith("Third question text.")


def test_write_jsonl_writes_one_json_object_per_line(tmp_path):
    path = tmp_path / "questions.jsonl"
    records = [
        {"question_id": "2003-001", "answer": ""},
        {"question_id": "2003-002", "answer": ""},
    ]

    write_jsonl(records, path)

    lines = path.read_text().splitlines()
    assert [json.loads(line)["question_id"] for line in lines] == [
        "2003-001",
        "2003-002",
    ]


def test_write_audit_files_writes_markdown_and_tsv_by_year(tmp_path):
    records = [
        {
            "question_id": "2003-001",
            "year": 2003,
            "question_number": 1,
            "question_text": "A complete question?\nA. Alpha\nB. Beta\nC. Gamma\nD. Delta\nE. Epsilon",
            "source_page_start": 1,
            "source_page_end": 1,
        },
        {
            "question_id": "2003-002",
            "year": 2003,
            "question_number": 2,
            "question_text": "Too short.\nA. Alpha",
            "source_page_start": 1,
            "source_page_end": 2,
        },
        {
            "question_id": "2004-001",
            "year": 2004,
            "question_number": 1,
            "question_text": "10 % Ecology 5 questions\nA. Alpha\nB. Beta",
            "source_page_start": 3,
            "source_page_end": 3,
        },
    ]

    result = write_audit_files(records, tmp_path)

    assert result == {"year_count": 2, "file_count": 4}

    markdown_2003 = (tmp_path / "2003.md").read_text(encoding="utf-8")
    assert "| 2003-001 | 1 | 1-1 | ok |" in markdown_2003
    assert "| 2003-002 | 2 | 1-2 | missing_choices:B,C,D,E |" in markdown_2003

    tsv_2004 = (tmp_path / "2004.tsv").read_text(encoding="utf-8")
    assert tsv_2004.splitlines()[0] == (
        "question_id\tyear\tquestion_number\tpages\twarnings\tpreview"
    )
    assert "2004-001\t2004\t1\t3-3\tsection_header,missing_choices:C,D,E\t" in tsv_2004
