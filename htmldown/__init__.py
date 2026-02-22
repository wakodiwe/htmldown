#!/usr/bin/env python3
"""
Fetch HTML from URL, extract main body content, and save as readable Markdown.
"""

import re
import subprocess
from urllib.parse import urlparse
from readability import Document
import html2text
from bs4 import BeautifulSoup
import chardet


def fetch_html(url: str) -> str:
    """Fetch HTML content from URL using curl."""
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", url],
        capture_output=True,
        text=True,
        timeout=35,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return result.stdout


def extract_filename(url: str) -> str:
    """Extract filename from URL."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        hostname = parsed.netloc.replace("www.", "")
        return hostname.split(".")[0]
    filename = path.split("/")[-1]
    if "." in filename:
        filename = filename.rsplit(".", 1)[0]
    return filename or "output"


def html_to_markdown(html_content: str, base_url: str = "") -> str:
    """Extract main body and convert to readable Markdown."""
    doc = Document(html_content)
    body_html = doc.summary()

    if not body_html or body_html == "<html><body></body></html>":
        soup = BeautifulSoup(html_content, "html.parser")
        body = soup.find("body")
        if body:
            body_html = str(body)
        else:
            body_html = html_content

    h = html2text.HTML2Text()
    h.body_width = 80
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.single_line_break = False
    h.baseurl = base_url

    markdown = h.handle(body_html)

    markdown = re.sub(r"\[([^\]]+)\]\(([^#]+)#([^)]+)\)", r"[\1](\2)", markdown)
    markdown = re.sub(r"\[([^\]]+)\]\((#[^)]+)\)", r"[\1](\2)", markdown)

    title = doc.title()
    if title:
        markdown = f"# {title}\n\n{markdown}"

    return markdown


def fetch_and_convert(url: str, output_path: str | None = None) -> str:
    """Fetch URL and convert to Markdown, optionally save to file."""
    html_content = fetch_html(url)
    markdown = html_to_markdown(html_content, url)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

    return markdown


def fetch_to_file(url: str, output_dir: str = ".") -> str:
    """Fetch URL and save Markdown file. Returns output filepath."""
    filename = extract_filename(url)
    html_content = fetch_html(url)
    markdown = html_to_markdown(html_content, url)

    output_path = f"{output_dir}/{filename}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    return output_path
