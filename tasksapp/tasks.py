import os
import re
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Iterable

from celery import shared_task
from django.conf import settings
import fitz  # PyMuPDF
from PIL import Image


@shared_task
def add(x: int, y: int) -> int:
    time.sleep(2)
    return x + y


@shared_task
def count_words(text: str) -> int:
    time.sleep(1)
    return len([w for w in text.split() if w])


def _iter_pdfs(directory: Path) -> Iterable[Path]:
    if not directory.exists():
        return []
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix.lower() == '.pdf':
            yield entry


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r'[^a-z0-9\-\_]+', '-', value)
    value = re.sub(r'-{2,}', '-', value).strip('-')
    return value or 'deck'


@shared_task
def scan_slides_folder() -> int:
    """Scan the watch folder and enqueue processing for each PDF found.

    Returns number of PDFs enqueued.
    """
    watch_dir: Path = Path(getattr(settings, 'SLIDES_WATCH_DIR', Path('incoming_slides')))
    enqueued = 0
    for pdf_path in _iter_pdfs(watch_dir):
        process_pdf.delay(str(pdf_path))
        enqueued += 1
    return enqueued


@shared_task
def process_pdf(pdf_path_str: str) -> dict:
    """Process a PDF: compute output directory and enqueue per-page conversion.

    For now, this stubs the actual per-page conversion and just computes the
    destination directory where Markdown will be written by downstream tasks.
    """
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        return {'ok': False, 'error': 'missing_file', 'path': pdf_path_str}

    # Compute deck slug and dated directory
    today = datetime.utcnow().strftime('%Y-%m-%d')
    deck_slug = _slugify(pdf_path.stem)
    content_root: Path = Path(getattr(settings, 'SLIDES_CONTENT_DIR', Path('content')))
    deck_dir = content_root / 'default-course' / today / deck_slug
    assets_dir = deck_dir / 'assets'
    os.makedirs(assets_dir, exist_ok=True)

    # Simple manifest with file hash for idempotency
    sha256 = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    manifest = {
        'source_path': str(pdf_path.resolve()),
        'sha256': sha256,
        'deck_dir': str(deck_dir.resolve()),
    }

    # Open PDF and enqueue per-page conversions
    with fitz.open(pdf_path) as doc:
        total_pages = doc.page_count
        for page_index in range(total_pages):
            convert_page_to_markdown.delay(
                str(pdf_path),
                page_index,
                str(deck_dir),
                total_pages,
            )
    manifest['total_pages'] = total_pages
    return {'ok': True, 'manifest': manifest}


@shared_task
def convert_page_to_markdown(pdf_path_str: str, page_index: int, deck_dir_str: str, total_pages: int) -> dict:
    """Convert a single PDF page to Markdown plus extracted images.

    Produces slide-XXX.md with YAML frontmatter and references to extracted images.
    """
    deck_dir = Path(deck_dir_str)
    assets_root = deck_dir / 'assets' / f'slide-{page_index+1:03d}'
    os.makedirs(assets_root, exist_ok=True)

    with fitz.open(pdf_path_str) as doc:
        page = doc.load_page(page_index)
        text = page.get_text('text') or ''

        # Extract images
        image_paths: list[str] = []
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            img_out = assets_root / f'fig-{img_index+1}.png'
            if pix.alpha:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            pix.save(str(img_out))
            image_paths.append(str(img_out.relative_to(deck_dir)))

    # Basic cleanup for markdown
    cleaned = re.sub(r'[\r\t]+', ' ', text)
    cleaned = re.sub(r'\s+\n', '\n', cleaned)

    # Build frontmatter and body
    slide_number = page_index + 1
    md_lines = [
        '---',
        f'slideIndex: {slide_number}',
        f'totalSlides: {total_pages}',
        '---',
        '',
    ]
    if cleaned.strip():
        md_lines.append(cleaned.strip())
        md_lines.append('')
    for rel_path in image_paths:
        md_lines.append(f'![figure]({rel_path.replace("\\", "/")})')

    out_md = deck_dir / f'slide-{slide_number:03d}.md'
    out_md.write_text("\n".join(md_lines), encoding='utf-8')
    return {'ok': True, 'slide': slide_number, 'path': str(out_md)}

