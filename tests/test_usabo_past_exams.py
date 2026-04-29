from biobloom.usabo_past_exams import extract_filename_from_url
from biobloom.usabo_past_exams import filter_open_exam_urls
from biobloom.usabo_past_exams import rename_downloaded_open_exam_files_for_urls


def test_filter_open_exam_urls_keeps_exams_and_keys():
    urls = [
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam.pdf",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam_Key.pdf",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2004_OpenExam_Answer_Key.pdf",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/semifinal/2003_SemifinalExam.pdf",
    ]

    assert filter_open_exam_urls(urls) == [
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam.pdf",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam_Key.pdf",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2004_OpenExam_Answer_Key.pdf",
    ]


def test_filter_open_exam_urls_keeps_2013_to_2018_patterns():
    urls = [
        "https://www.usabo-trc.org/sites/default/files/2013%20USABO%20Open%20Exam%20Final%20without%20%20Answers.pdf",
        "https://www.usabo-trc.org/sites/default/files/2013%20USABO%20Open%20Exam%20Answers.pdf",
        "https://www.usabo-trc.org/sites/default/files/allfiles/USABO%2017%20OE%20Key.pdf",
        "https://www.usabo-trc.org/sites/default/files/USABO%2014%20Semifinal%20Final.pdf",
    ]

    assert filter_open_exam_urls(urls) == [
        "https://www.usabo-trc.org/sites/default/files/2013%20USABO%20Open%20Exam%20Final%20without%20%20Answers.pdf",
        "https://www.usabo-trc.org/sites/default/files/2013%20USABO%20Open%20Exam%20Answers.pdf",
        "https://www.usabo-trc.org/sites/default/files/allfiles/USABO%2017%20OE%20Key.pdf",
    ]


def test_filter_open_exam_urls_normalizes_and_deduplicates():
    urls = [
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam.pdf?download=1",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam.pdf#page=1",
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam.pdf",
    ]

    assert filter_open_exam_urls(urls) == [
        "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam.pdf",
    ]


def test_extract_filename_from_url_uses_path_basename():
    url = "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2003_OpenExam_Key.pdf?download=1"

    assert extract_filename_from_url(url) == "2003_OpenExam_Key.pdf"


def test_extract_filename_from_url_normalizes_2012_spacing():
    url = "https://www.usabo-trc.org/sites/default/files/images/pdf/exams/openexam/2012_Open%20Exam.pdf"

    assert extract_filename_from_url(url) == "2012_OpenExam.pdf"


def test_extract_filename_from_url_normalizes_2013_to_2018_names():
    assert extract_filename_from_url(
        "https://www.usabo-trc.org/sites/default/files/2013%20USABO%20Open%20Exam%20Answers.pdf"
    ) == "2013_OpenExam_AnsKey.pdf"
    assert extract_filename_from_url(
        "https://www.usabo-trc.org/sites/default/files/USABO%2014%20Open%20Exam%20Final.pdf"
    ) == "2014_OpenExam.pdf"
    assert extract_filename_from_url(
        "https://www.usabo-trc.org/sites/default/files/USABO%2014%20Open%20Exam%20Final%20ans.pdf"
    ) == "2014_OpenExam_AnsKey.pdf"
    assert extract_filename_from_url(
        "https://www.usabo-trc.org/sites/default/files/USABO%20Open%20Exam.Finalwans.pdf"
    ) == "2015_OpenExam_AnsKey.pdf"
    assert extract_filename_from_url(
        "https://www.usabo-trc.org/sites/default/files/allfiles/USABO%2017%20OE%20Key.pdf"
    ) == "2017_OpenExam_AnsKey.pdf"
    assert extract_filename_from_url(
        "https://www.usabo-trc.org/sites/default/files/allfiles/ctools/USABO%2018%20Open%20Exam.Final%20w.ans_0.pdf"
    ) == "2018_OpenExam_AnsKey.pdf"


def test_rename_downloaded_open_exam_files_for_urls_renames_weird_files(tmp_path):
    exam_url = "https://www.usabo-trc.org/sites/default/files/USABO%20Open%20Exam.Finalwoans_1.pdf"
    key_url = "https://www.usabo-trc.org/sites/default/files/USABO%20Open%20Exam.Finalwans.pdf"
    exam_path = tmp_path / "USABO Open Exam.Finalwoans_1.pdf"
    key_path = tmp_path / "USABO Open Exam.Finalwans.pdf"
    exam_path.write_bytes(b"exam")
    key_path.write_bytes(b"key")

    renamed = rename_downloaded_open_exam_files_for_urls([exam_url, key_url], tmp_path)

    assert [path.name for path in renamed] == [
        "2015_OpenExam.pdf",
        "2015_OpenExam_AnsKey.pdf",
    ]
    assert not exam_path.exists()
    assert not key_path.exists()
    assert (tmp_path / "2015_OpenExam.pdf").read_bytes() == b"exam"
    assert (tmp_path / "2015_OpenExam_AnsKey.pdf").read_bytes() == b"key"
