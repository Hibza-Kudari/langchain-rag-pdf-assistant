from pypdf import PdfReader

reader = PdfReader("documents/DIP_4.pdf")

full_text = ""

for page in reader.pages:
    full_text += page.extract_text()

print(full_text[:1000])
print("Characters:", len(full_text))