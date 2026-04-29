"""Utilities for extracting and downloading USABO Open Exam PDFs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
from typing import Optional
from urllib.parse import unquote
from urllib.parse import urlsplit
from urllib.parse import urlunsplit
import re

import fire
from loguru import logger
import pymupdf
import requests

_YEARLESS_CANONICAL_FILENAMES = {
    "2012_Open Exam.pdf": "2012_OpenExam.pdf",
    "USABO Open Exam.Finalwoans_1.pdf": "2015_OpenExam.pdf",
    "USABO Open Exam.Finalwans.pdf": "2015_OpenExam_AnsKey.pdf",
}


def normalize_pdf_url(url: str) -> str:
    """Remove query and fragment components so duplicate links collapse cleanly."""
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def extract_filename_from_url(url: str) -> str:
    """Return the local filename for a downloaded PDF."""
    normalized = normalize_pdf_url(url)
    raw_filename = Path(unquote(urlsplit(normalized).path)).name
    if not raw_filename:
        raise ValueError(f"URL does not end with a filename: {url}")
    return canonical_open_exam_filename(raw_filename)


def canonical_open_exam_filename(raw_filename: str) -> str:
    """Normalize later-year Open Exam files to the local naming convention."""
    if raw_filename in _YEARLESS_CANONICAL_FILENAMES:
        return _YEARLESS_CANONICAL_FILENAMES[raw_filename]

    year = infer_open_exam_year(raw_filename)
    if year is None or year < 2013:
        return raw_filename

    suffix = "_AnsKey.pdf" if is_answer_key_filename(raw_filename) else ".pdf"
    return f"{year}_OpenExam{suffix}"


def infer_open_exam_year(raw_filename: str) -> Optional[int]:
    """Infer the exam year from a USABO Open Exam filename."""
    year_match = re.search(r"\b(20\d{2})\b", raw_filename)
    if year_match:
        return int(year_match.group(1))

    short_year_match = re.search(r"\b(\d{2})\b", raw_filename)
    if short_year_match:
        return 2000 + int(short_year_match.group(1))

    return None


def is_answer_key_filename(raw_filename: str) -> bool:
    """Classify whether a raw Open Exam filename is an answer key."""
    compact = _compact_text(raw_filename)
    if any(marker in compact for marker in ("withoutanswers", "woans", "woanswers")):
        return False
    return any(marker in compact for marker in ("answer", "anskey", "key", "wans", "anspdf"))


def _compact_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def is_open_exam_pdf_url(url: str) -> bool:
    """Keep only URLs that refer to Open Exam PDFs, including answer keys."""
    normalized = normalize_pdf_url(url)
    path = unquote(urlsplit(normalized).path)
    if not path.lower().endswith(".pdf"):
        return False

    lowered = path.lower()
    if "semifinal" in lowered:
        return False

    compact = _compact_text(path)
    if "openexam" in compact:
        return True

    return bool(re.search(r"\boe\b", lowered) and "key" in lowered)


def filter_open_exam_urls(urls: Iterable[str]) -> list[str]:
    """Normalize, filter, and deduplicate Open Exam PDF URLs while preserving order."""
    filtered: list[str] = []
    seen: set[str] = set()
    for url in urls:
        normalized = normalize_pdf_url(url)
        if not is_open_exam_pdf_url(normalized):
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        filtered.append(normalized)
    return filtered


def rename_downloaded_open_exam_files_for_urls(
    urls: Iterable[str],
    output_dir: str | Path,
) -> list[Path]:
    """Rename previously downloaded files to their canonical local filenames."""
    destination_dir = Path(output_dir)
    renamed: list[Path] = []

    for url in urls:
        normalized = normalize_pdf_url(url)
        raw_filename = Path(unquote(urlsplit(normalized).path)).name
        canonical_filename = extract_filename_from_url(normalized)
        if raw_filename == canonical_filename:
            continue

        source = destination_dir / raw_filename
        destination = destination_dir / canonical_filename
        if not source.exists():
            continue
        if destination.exists():
            logger.info("Skipping rename because destination exists: {}", destination)
            continue

        source.rename(destination)
        logger.info("Renamed {} -> {}", source.name, destination.name)
        renamed.append(destination)

    return renamed


def extract_pdf_links(pdf_path: str | Path) -> list[str]:
    """Extract all external URI links from a PDF."""
    links: list[str] = []
    document = pymupdf.open(str(pdf_path))
    try:
        for page in document:
            for link in page.links(kinds=(pymupdf.LINK_URI,)):
                uri = link.get("uri")
                if uri:
                    links.append(uri)
    finally:
        document.close()
    return links


def download_pdf(
    url: str,
    output_dir: str | Path,
    *,
    session: Optional[requests.Session] = None,
    overwrite: bool = False,
    timeout: float = 30.0,
) -> Path:
    """Download one PDF into the target directory."""
    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / extract_filename_from_url(url)

    if destination.exists() and not overwrite:
        logger.info("Skipping existing file: {}", destination)
        return destination

    client = session or requests.Session()
    headers = {"User-Agent": "biobloom-usabo-ingest/0.1"}

    logger.info("Downloading {}", url)
    response = client.get(url, stream=True, timeout=timeout, headers=headers)
    response.raise_for_status()

    with destination.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 128):
            if chunk:
                handle.write(chunk)

    logger.info("Saved {}", destination)
    return destination


def download_open_exam_pdfs(
    source_pdf: str | Path,
    output_dir: str | Path,
    *,
    overwrite: bool = False,
    timeout: float = 30.0,
) -> list[Path]:
    """Extract Open Exam URLs from the source PDF and download the linked PDFs."""
    all_links = extract_pdf_links(source_pdf)
    open_exam_urls = filter_open_exam_urls(all_links)

    if not open_exam_urls:
        raise ValueError(f"No Open Exam PDF links found in {source_pdf}")

    logger.info(
        "Found {} Open Exam PDF links in {}",
        len(open_exam_urls),
        source_pdf,
    )

    downloaded: list[Path] = []
    with requests.Session() as session:
        for url in open_exam_urls:
            downloaded.append(
                download_pdf(
                    url,
                    output_dir,
                    session=session,
                    overwrite=overwrite,
                    timeout=timeout,
                )
            )
    return downloaded


def rename_downloaded_open_exam_files(
    source_pdf: str | Path,
    output_dir: str | Path,
) -> list[Path]:
    """Rename downloaded Open Exam PDFs based on the URLs found in the source PDF."""
    open_exam_urls = filter_open_exam_urls(extract_pdf_links(source_pdf))
    return rename_downloaded_open_exam_files_for_urls(open_exam_urls, output_dir)


class UsaboPastExamCli:
    """CLI entry points for USABO past exam ingestion."""

    def extract_links(self, source_pdf: str) -> list[str]:
        return extract_pdf_links(source_pdf)

    def list_open_exam_urls(self, source_pdf: str) -> list[str]:
        return filter_open_exam_urls(extract_pdf_links(source_pdf))

    def download_open_exams(
        self,
        source_pdf: str = "raw/official_past_exams/USABO_Past_Exams_0.pdf",
        output_dir: str = "raw/official_past_exams",
        overwrite: bool = False,
        timeout: float = 30.0,
    ) -> list[str]:
        downloaded = download_open_exam_pdfs(
            source_pdf,
            output_dir,
            overwrite=overwrite,
            timeout=timeout,
        )
        return [str(path) for path in downloaded]

    def rename_open_exam_files(
        self,
        source_pdf: str = "raw/official_past_exams/USABO_Past_Exams_0.pdf",
        output_dir: str = "raw/official_past_exams",
    ) -> list[str]:
        renamed = rename_downloaded_open_exam_files(source_pdf, output_dir)
        return [str(path) for path in renamed]


def main() -> None:
    fire.Fire(UsaboPastExamCli)


if __name__ == "__main__":
    main()
