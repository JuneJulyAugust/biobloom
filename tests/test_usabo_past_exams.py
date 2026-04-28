from biobloom.usabo_past_exams import extract_filename_from_url
from biobloom.usabo_past_exams import filter_open_exam_urls


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
