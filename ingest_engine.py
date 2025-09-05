# ingest_data.py (Final Robust Version)
import os
import re
import json
import torch
import pypdf
from sentence_transformers import SentenceTransformer

# --- Config ---
PDF_SOURCE_FOLDER = 'books'
EMBEDDINGS_FILE = 'embeddings.pt'
CHUNKS_FILE = 'text_chunks.json'
MODEL_NAME = 'all-MiniLM-L6-v2'

# Delete old files
for f in [EMBEDDINGS_FILE, CHUNKS_FILE]:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed old file: {f}")

# --- Text Extraction & Cleaning ---
def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file."""
    full_text = ""
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + " "
    except Exception as e:
        print(f"⚠️ Could not read {os.path.basename(pdf_path)}. Error: {e}")
    return full_text

def advanced_text_cleaning(text):
    """Cleans text and heuristically splits table-like structures into sentences."""
    text = re.sub(r'\s+', ' ', text).replace('\f', ' ')
    blocks = re.split(r'(?<=[.!?])\s+', text)
    processed_text = ""
    for block in blocks:
        digits = sum(c.isdigit() for c in block)
        letters = sum(c.isalpha() for c in block)
        if letters > 10 and digits > 5:
            if not block.endswith('.'):
                block += '.'
        processed_text += block + " "
    return processed_text.strip()

def create_text_chunks(text, chunk_size=800, chunk_overlap=100):
    """Splits long text into overlapping semantic chunks."""
    if not text:
        return []

    cleaned_text = advanced_text_cleaning(text)
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)

    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            overlap_text = " ".join(current_chunk.split()[-chunk_overlap:])
            current_chunk = overlap_text + " " + sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Filter out very small chunks
    return [c for c in chunks if len(c) > 100]

# --- Main Ingestion Process ---
all_text_chunks = []
book_chunk_report = {}

print(f"\n📂 Scanning folder: {PDF_SOURCE_FOLDER}")
pdf_files = [f for f in os.listdir(PDF_SOURCE_FOLDER) if f.lower().endswith('.pdf')]
if not pdf_files:
    print("❌ No PDF files found in the folder.")
    exit()

for pdf_file in pdf_files:
    pdf_path = os.path.join(PDF_SOURCE_FOLDER, pdf_file)
    print(f"\n📖 Processing: {pdf_file}")
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text.strip():
        print(f"⚠️ No text extracted from {pdf_file}. Skipping.")
        continue

    chunks = create_text_chunks(raw_text)
    print(f"✅ Extracted {len(chunks)} chunks from {pdf_file}")

    all_text_chunks.extend(chunks)
    book_chunk_report[pdf_file] = len(chunks)

if not all_text_chunks:
    print("❌ No valid text chunks could be created. Stopping.")
    exit()

# --- Report ---
print("\n📊 Ingestion Report:")
for book, count in book_chunk_report.items():
    print(f"   - {book}: {count} chunks")
print(f"   Total chunks: {len(all_text_chunks)}")
print("-----------------------------------\n")

# --- Generate Embeddings ---
print(f"⚙️ Loading model '{MODEL_NAME}'...")
model = SentenceTransformer(MODEL_NAME)

print("🔍 Generating embeddings (this may take a while)...")
embeddings = model.encode(all_text_chunks, convert_to_tensor=True, show_progress_bar=True)

# --- Save Results ---
torch.save(embeddings, EMBEDDINGS_FILE)
print(f"💾 Embeddings saved to '{EMBEDDINGS_FILE}'")

with open(CHUNKS_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_text_chunks, f)
print(f"💾 Text chunks saved to '{CHUNKS_FILE}'")

print("\n✅ Ingestion complete! Your chatbot is ready.")
