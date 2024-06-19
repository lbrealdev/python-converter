#!/usr/bin/env python

import sys
from pathlib import Path
import pypandoc


if len(sys.argv) < 2:
    print("Usage: python converter.py <path-to-markdown>")
    sys.exit(1)

SOURCE_PATH_TO_MD = Path(sys.argv[1])
DESTINATION_PATH_TO_PDF = Path(SOURCE_PATH_TO_MD) / "_output"

if not SOURCE_PATH_TO_MD.exists() or not SOURCE_PATH_TO_MD.is_dir():
    print("Invalid path to markdown directory!")
    sys.exit(1)

if not DESTINATION_PATH_TO_PDF.exists():
    DESTINATION_PATH_TO_PDF.mkdir()

markdown_files = list(SOURCE_PATH_TO_MD.rglob("*.md"))

if not markdown_files:
    print(f"No markdown files found in {SOURCE_PATH_TO_MD}")
    sys.exit(1)

source_md_files = []
output_pdf_files = []

print("converter from markdown to PDF\n")
for markdown_file in markdown_files:
    relative_path = markdown_file.relative_to(SOURCE_PATH_TO_MD)
    pdf_output_path = DESTINATION_PATH_TO_PDF / relative_path.with_suffix(".pdf")

    pdf_output_path.parent.mkdir(parents=True, exist_ok=True)

    source_md_files.append(markdown_file)
    output_pdf_files.append(pdf_output_path)

    try:
        pypandoc.convert_file(
            str(markdown_file),
            'pdf',
            outputfile=str(pdf_output_path),
            extra_args=[
                '--pdf-engine=pdflatex',
                '--from=markdown+rebase_relative_paths'
            ]
        )
    except Exception as e:
        print(f"Error converting {markdown_file}: {e}")
        sys.exit(1)

print("Source markdown files:")
for input_md in source_md_files:
    print(input_md)

print("\nOutput PDF files:")
for output_pdf in output_pdf_files:
    print(output_pdf)
