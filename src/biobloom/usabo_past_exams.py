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


def normalize_pdf_url(url: str) -> str:
    """Remove query and fragment components so duplicate links collapse cleanly."""
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def extract_filename_from_url(url: str) -> str:
    """Return the upstream PDF filename."""
    normalized = normalize_pdf_url(url)
    filename = Path(unquote(urlsplit(normalized).path)).name
    if not filename:
        raise ValueError(f"URL does not end with a filename: {url}")
    return filename


def _compact_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def is_open_exam_pdf_url(url: str) -> bool:
    """Keep only URLs that refer to Open Exam PDFs, including answer keys."""
    normalized = normalize_pdf_url(url)
    path = urlsplit(normalized).path
    if not path.lower().endswith(".pdf"):
        return False
    return "openexam" in _compact_text(path)


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


def main() -> None:
    fire.Fire(UsaboPastExamCli)


if __name__ == "__main__":
    main()
