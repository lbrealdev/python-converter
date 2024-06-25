#!/usr/bin/env python

import os
import sys
import shutil
from pathlib import Path
import pypandoc
import re


if len(sys.argv) < 2:
    print("Usage: python converter.py <path-to-markdown>")
    sys.exit(1)


# install_pandoc function
def install_pandoc():
    pandoc_bin = shutil.which("pandoc")
    if not pandoc_bin:
        from pypandoc.pandoc_download import download_pandoc

        print("Pandoc binary was not found!")

        # Set the environment variable PYPANDOC_PANDOC
        # to the only location where pandoc will be searched
        os.environ.setdefault("PYPANDOC_PANDOC", "/usr/bin/pandoc")

        # Pandoc binary installation and download directory.
        bin_dir = Path(os.path.join(os.sep, "usr", "bin"))
        tmp_dir = Path(os.path.join(os.sep, "tmp"))

        print(f"Downloading pandoc to {tmp_dir} and installing it in {bin_dir} ...\n")
        download_pandoc(targetfolder=str(bin_dir), download_folder=str(tmp_dir))


# convert_pandoc function
def convert_pandoc(input, output, auth: bool = False):
    markdown = str(input)
    pdf = str(output)

    args = [
        "--pdf-engine=pdflatex",
        "--from=markdown-implicit_figures+rebase_relative_paths",
        "--extract-media=.",
    ]

    if auth:
        args.append(f"--request-header=Authorization: token {GITHUB_AUTH_TOKEN}")

    pypandoc.convert_file(markdown, "pdf", outputfile=pdf, extra_args=args)


def search_markdown(path):
    md_element_image_url_pattern = r"^[!]?\[.*?\]\((https:\/\/[^\)]+\.(?:png|jpg|jpeg|gif|bmp|svg))\)"
    md_url_asset_pattern = r'/asset/'
    md_comment_pattern = r"\[.*?\]: <>"

    md_pattern_found = False
    md_with_comment = False

    for file in path.rglob("*.md"):
        with file.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        count = 1

        for line in lines:
            if re.search(md_comment_pattern, line):
                md_with_comment = True

        if md_with_comment:
            break

        for line in lines:
            match_pattern = re.match(md_element_image_url_pattern, line)
            if match_pattern:
                asset = match_pattern.group(0)
                if re.search(md_url_asset_pattern, asset):
                    new_comment_pattern = f"[comment{count:03}]: <> ({asset})\n"
                    update_string = re.sub(md_element_image_url_pattern, new_comment_pattern, asset)
                    new_lines.append(update_string)
                    md_pattern_found = True
                    count += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            
            with file.open("w", encoding="utf-8") as f:
                f.writelines(new_lines)
                
    if md_pattern_found and not md_with_comment:
        print("Markdown image URL element found, editing file to convert!")
        print()
    if not md_pattern_found and md_with_comment:
        print(f"The markdown file already has comments in asset references, nothing to do!")
        print()
    if not md_pattern_found and not md_with_comment:
        pass

# Set the environment variable GITHUB_TOKEN to github authenticate.
# This variable must be set if the markdown files you want
# convert to PDF contain images with URL image referencing an
# image in a private repository.
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_AUTH = bool(GITHUB_AUTH_TOKEN)

# Path to the directory where the markdown and
# destination path that will be created '_output' for converted pdf files.
SOURCE_PATH_TO_MD = Path(sys.argv[1])
DESTINATION_PATH_TO_PDF = Path(SOURCE_PATH_TO_MD) / "_output"


if not SOURCE_PATH_TO_MD.exists() or not SOURCE_PATH_TO_MD.is_dir():
    print("Invalid path to markdown directory!")
    sys.exit(1)

markdown_files = list(SOURCE_PATH_TO_MD.rglob("*.md"))
source_md_files = []
output_pdf_files = []

if not markdown_files:
    print(f"No markdown files found in {SOURCE_PATH_TO_MD}")
    sys.exit(1)

if not DESTINATION_PATH_TO_PDF.exists():
    DESTINATION_PATH_TO_PDF.mkdir()

install_pandoc()
search_markdown(SOURCE_PATH_TO_MD)

print(f"Markdown input directory: {SOURCE_PATH_TO_MD.absolute()}")
print(f"PDF output directory: {DESTINATION_PATH_TO_PDF.absolute()}")
print(f"Markdown files found: {len(markdown_files)}")
print()
print("Converting markdown files to PDF ...\n")
for markdown_file in markdown_files:
    relative_path = markdown_file.relative_to(SOURCE_PATH_TO_MD)
    pdf_output_path = DESTINATION_PATH_TO_PDF / relative_path.with_suffix(".pdf")

    pdf_output_path.parent.mkdir(parents=True, exist_ok=True)

    source_md_files.append(markdown_file)
    output_pdf_files.append(pdf_output_path)

    try:
        convert_pandoc(input=markdown_file, output=pdf_output_path, auth=GITHUB_AUTH)
    except Exception as e:
        print(f"Error converting {markdown_file.absolute()}: {e}")
        sys.exit(1)

print("Source markdown files:")
for input_md in source_md_files:
    print(input_md.absolute())

print("\nOutput PDF files:")
for output_pdf in output_pdf_files:
    print(output_pdf.absolute())
