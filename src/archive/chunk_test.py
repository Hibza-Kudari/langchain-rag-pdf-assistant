from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

reader = PdfReader("documents/DIP_4.pdf")

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    
    if text:
        full_text += text

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(full_text)

print("Number of chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])