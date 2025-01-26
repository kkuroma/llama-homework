import argparse
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

import pytesseract
from pdf2image import pdfinfo_from_path, convert_from_path
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF and summarize using AI models.")

    # Command-line arguments
    parser.add_argument("--summary_format_files", type=str, default="prompts/summary_format.txt", help="Path to the summary format file")
    parser.add_argument("--prompt_file", type=str, default="prompts/story_summary.txt", help="Path to the prompt file")
    parser.add_argument("--use_gpt", type=bool, default=True, help="Whether to use GPT-based model (True) or LLaMA (False)")
    parser.add_argument("--pdf_file", type=str, required=True, help="Path to the input PDF file")
    parser.add_argument("--output_file", type=str, default="outputs/summary.txt", help="Path to the output text file")
    parser.add_argument("--chunk_size", type=int, default=5, help="Number of pages to process at once")

    args = parser.parse_args()

    # Select language model
    if args.use_gpt:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
    else:
        llm = ChatOllama(model="llama3.2", temperature=0)

    # Extract PDF information
    info = pdfinfo_from_path(args.pdf_file, userpw=None, poppler_path=None)
    max_pages = info["Pages"]
    
    page_data = []
    for page in tqdm(range(1, max_pages + 1), desc="Extracting text from PDF"):
        page_img = convert_from_path(args.pdf_file, dpi=200, first_page=page, last_page=page)[0]
        page_text = pytesseract.image_to_string(page_img)
        page_data.append(page_text)

    # Read prompt and format files
    with open(args.prompt_file, 'r') as file:
        prompt_txt = file.read()
    with open(args.summary_format_files, 'r') as file:
        summary_format = file.read()

    prompt = PromptTemplate(
        template=prompt_txt,
        input_variables=["summary", "summary_format", "story"],
    )
    
    rag_chain = prompt | llm | StrOutputParser()
    summary = ""

    for i in tqdm(range(0, len(page_data), args.chunk_size), desc="Summarizing text"):
        story_chunk = "".join(page_data[i:min(i + args.chunk_size, len(page_data))])
        summary = rag_chain.invoke({
            "summary": summary,
            "summary_format": summary_format,
            "story": story_chunk
        })

    # Save the summary to the output file
    with open(args.output_file, "w") as text_file:
        text_file.write(summary)
    
    print(f"Summary saved to {args.output_file}")

if __name__ == "__main__":
    main()