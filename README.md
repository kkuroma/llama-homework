# LLaMa Homework Agent
Local LLaMa RAG to help with homework through locally-saved textbooks. The scripts extract text from a PDF file and generates a summary using AI models (GPT or LLaMA).

## Installation

Ensure you have the required dependencies installed:

```bash
pip install langchain_community langchain_openai pytesseract pdf2image tqdm
```

Additionally, install **Tesseract OCR** and **Poppler**:

- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt install tesseract-ocr poppler-utils
  ```
- **MacOS:**
  ```bash
  brew install tesseract poppler
  ```
- **Windows:**
  1. Download and install Tesseract from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
  2. Download and install Poppler from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases).
  3. Add both to your system PATH.

## Usage

Run the script using the following command:

```bash
python script.py --pdf_file path/to/input.pdf --output_file path/to/output.txt
```

### Available Command-line Arguments:

| Argument                | Description                              | Default Value                   |
|------------------------|------------------------------------------|---------------------------------|
| `--summary_format_files` | Path to the summary format file          | `prompts/summary_format.txt`    |
| `--prompt_file`          | Path to the prompt template file         | `prompts/story_summary.txt`     |
| `--use_gpt`              | Use GPT-based model (True) or LLaMA (False) | `True`                          |
| `--pdf_file`             | Path to the input PDF file (Required)    | _No Default (Required)_         |
| `--output_file`          | Path to save the output text summary     | `outputs/summary.txt`           |
| `--chunk_size`           | Number of pages to process at once       | `5`                             |

### Example Commands:

1. **Summarize using GPT (default):**
   ```bash
   python script.py --pdf_file myfile.pdf --output_file mysummary.txt
   ```

2. **Summarize using LLaMA:**
   ```bash
   python script.py --pdf_file myfile.pdf --output_file mysummary.txt --use_gpt False
   ```

3. **Process PDF in chunks of 10 pages:**
   ```bash
   python script.py --pdf_file myfile.pdf --chunk_size 10
   ```

## Troubleshooting

- Ensure `Tesseract` and `Poppler` are installed and properly configured in your environment.
- For large PDFs, increase system memory or reduce `--chunk_size`.