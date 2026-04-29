import json

from biobloom.usabo_calibration_bank import extract_question_records_from_text
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
