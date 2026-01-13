
import os
from langchain_community.document_loaders import PyPDFLoader

def inspect_pdf():
    pdf_path = os.path.join("data", "docs", "Nigeria-Tax-Act-2025.pdf")
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print(f"Loading {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    keywords = ["monthly", "installment", "due date", "remittance", "filing", "cit", "paye", "pit"]
    
    print(f"Searching for keywords: {keywords}\n")
    
    with open("found_keywords.txt", "w", encoding="utf-8") as f:
        found_count = 0
        for page in pages:
            content = page.page_content.lower()
            for kw in keywords:
                if kw in content:
                    idx = content.find(kw)
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 200)
                    snippet = page.page_content[start:end].replace("\n", " ")
                    f.write(f"Found '{kw}' on page {page.metadata.get('page', '?')}:\n")
                    f.write(f"...{snippet}...\n")
                    f.write("-" * 40 + "\n")
                    found_count += 1
                    if found_count > 20:
                        f.write("Limit reached.\n")
                        return

    print("Done writing to found_keywords.txt")

    if found_count == 0:
        print("No keywords found.")

if __name__ == "__main__":
    inspect_pdf()
