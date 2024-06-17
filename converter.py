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

print("Convert MD to PDF:\n")
for markdown_file in markdown_files:
    relative_path = markdown_file.relative_to(SOURCE_PATH_TO_MD)
    pdf_output_path = DESTINATION_PATH_TO_PDF / relative_path.with_suffix('.pdf')
    
    try:
        #pypandoc.convert_file(
        #    str(markdown_file), 
        #    'pdf', 
        #    outputfile=str(pdf_file), 
        #    extra_args=['--pdf-engine=pdflatex']
        #)
        pdf_output_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_output_path.touch(exist_ok=True)
        print(f"{markdown_file} -> {pdf_output_path}")
    except Exception as e:
        print(f"Error converting {markdown_file}: {e}")
