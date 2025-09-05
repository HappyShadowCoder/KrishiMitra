<<<<<<< HEAD
# ingest_data.py (Improved with heuristic table row splitting)
=======
<<<<<<< HEAD
# ingest_data.py (Final, Robust Version)
=======
# ingest_data.py (Improved with heuristic table row splitting)
>>>>>>> dc692bf (Updated Chat Bot using LLM)
>>>>>>> recovered-work
import os
import pypdf
import torch
from sentence_transformers import SentenceTransformer
import json
import re

print("Starting robust data ingestion process...")

<<<<<<< HEAD
# --- Config ---
=======
<<<<<<< HEAD
# --- 1. Configuration ---
=======
# --- Config ---
>>>>>>> dc692bf (Updated Chat Bot using LLM)
>>>>>>> recovered-work
PDF_SOURCE_FOLDER = 'books'
EMBEDDINGS_FILE = 'embeddings.pt'
CHUNKS_FILE = 'text_chunks.json'
MODEL_NAME = 'all-MiniLM-L6-v2'

<<<<<<< HEAD
# Delete old files
=======
<<<<<<< HEAD
# Automatically delete old files
=======
# Delete old files
>>>>>>> dc692bf (Updated Chat Bot using LLM)
>>>>>>> recovered-work
for f in [EMBEDDINGS_FILE, CHUNKS_FILE]:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed old file: {f}")


<<<<<<< HEAD
=======
<<<<<<< HEAD
def extract_text_from_pdfs(folder_path):
    """Extracts raw text from all PDFs in a folder."""
    print(f"\nScanning for PDF files in '{folder_path}'...")
    full_text = ""
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("Error: No PDF files found.")
        return None
    for pdf_file in pdf_files:
        print(f"Processing '{pdf_file}'...")
        try:
            reader = pypdf.PdfReader(os.path.join(folder_path, pdf_file))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + " "
        except Exception as e:
            print(f"Warning: Could not read {pdf_file}. Error: {e}")
    return full_text


# --- NEW: Robust Text Chunking Function ---
def create_text_chunks(text, chunk_size=800, chunk_overlap=100):
    """
    Splits a long text into semantic chunks of a specified size.
    """
    if not text:
        return []

    # 1. Clean the text: replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    # 2. Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

=======
>>>>>>> recovered-work
def advanced_text_cleaning(text):
    """
    Cleans text by removing artifacts and, crucially, attempting to
    break up table-like structures into separate sentences.
    """
    # Consolidate whitespace and remove form feeds
    text = re.sub(r'\s+', ' ', text).replace('\f', ' ')

    # This is the key heuristic: Add a period to lines that seem like
    # table rows (e.g., contain numbers and don't already end a sentence).
    # We first split by potential sentence endings to process text blocks.
    blocks = re.split(r'(?<=[.!?])\s+', text)
    processed_text = ""
    for block in blocks:
        # If a block has many numbers and few letters, it's likely part of a table.
        digits = sum(c.isdigit() for c in block)
        letters = sum(c.isalpha() for c in block)
        if letters > 10 and digits > 5:  # Avoid processing very short strings
            # Add a period to force a sentence break
            if not block.endswith('.'):
                block += '.'
        processed_text += block + " "

    return processed_text.strip()


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
        print(f"⚠️ Warning: Could not read {os.path.basename(pdf_path)}. Error: {e}")
    return full_text


def create_text_chunks(text, chunk_size=800, chunk_overlap=100):
    """Splits long text into overlapping chunks."""
    if not text:
        return []

    # Use the advanced cleaning function here
    cleaned_text = advanced_text_cleaning(text)

    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)

    chunks, current_chunk = [], ""
<<<<<<< HEAD
=======
>>>>>>> dc692bf (Updated Chat Bot using LLM)
>>>>>>> recovered-work
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
<<<<<<< HEAD
=======
<<<<<<< HEAD
            # Create overlap
=======
>>>>>>> dc692bf (Updated Chat Bot using LLM)
>>>>>>> recovered-work
            overlap_text = " ".join(current_chunk.split()[-chunk_overlap:])
            current_chunk = overlap_text + " " + sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

<<<<<<< HEAD
=======
<<<<<<< HEAD
    # Filter out any chunks that are too small
    return [chunk for chunk in chunks if len(chunk) > 150]


# --- 2. Extract Text and Create Chunks ---
raw_text = extract_text_from_pdfs(PDF_SOURCE_FOLDER)
if not raw_text:
    print("Stopping script as no text could be extracted.")
    exit()

print(f"\nTotal characters extracted: {len(raw_text)}")

text_chunks = create_text_chunks(raw_text)

if not text_chunks:
    print("Error: No valid text chunks could be created from the PDF content.")
    exit()

print(f"Successfully created {len(text_chunks)} intelligent text chunks.")
print("\n--- Sample of first 3 text chunks ---")
for i, chunk in enumerate(text_chunks[:3]):
    print(f"Chunk {i + 1}: {chunk[:250]}...")
print("-------------------------------------\n")

# --- 3. Generate Embeddings ---
print(f"Loading sentence transformer model '{MODEL_NAME}'...")
model = SentenceTransformer(MODEL_NAME)
print("Generating embeddings for text chunks...")
embeddings = model.encode(text_chunks, convert_to_tensor=True, show_progress_bar=True)

# --- 4. Save the Results ---
torch.save(embeddings, EMBEDDINGS_FILE)
print(f"Embeddings saved to '{EMBEDDINGS_FILE}'")
with open(CHUNKS_FILE, 'w', encoding='utf-8') as f:
    json.dump(text_chunks, f)
print(f"Text chunks saved to '{CHUNKS_FILE}'")

print("\nIngestion complete! Your chatbot is ready.")
=======
>>>>>>> recovered-work
    return [c for c in chunks if len(c) > 100]


# --- Main script logic (remains the same as before) ---
all_text_chunks = []
book_chunk_report = {}

print(f"\n📂 Scanning folder: {PDF_SOURCE_FOLDER}")
pdf_files = [f for f in os.listdir(PDF_SOURCE_FOLDER) if f.lower().endswith('.pdf')]
if not pdf_files:
    print("❌ No PDF files found in 'books/' folder.")
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

# --- Step 2: Check results ---
if not all_text_chunks:
    print("❌ No valid text chunks could be created. Stopping.")
    exit()

print("\n📊 Ingestion Report:")
for book, count in book_chunk_report.items():
    print(f"   - {book}: {count} chunks")
print(f"   Total chunks: {len(all_text_chunks)}")
print("-----------------------------------\n")

# --- Step 3: Generate embeddings ---
print(f"⚙️ Loading model '{MODEL_NAME}'...")
model = SentenceTransformer(MODEL_NAME)

print("🔍 Generating embeddings (this may take a while)...")
embeddings = model.encode(all_text_chunks, convert_to_tensor=True, show_progress_bar=True)

# --- Step 4: Save results ---
torch.save(embeddings, EMBEDDINGS_FILE)
print(f"💾 Embeddings saved to '{EMBEDDINGS_FILE}'")

with open(CHUNKS_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_text_chunks, f)
print(f"💾 Text chunks saved to '{CHUNKS_FILE}'")

<<<<<<< HEAD
print("\n✅ Ingestion complete! Your chatbot is ready.")
=======
print("\n✅ Ingestion complete! Your chatbot is ready.")
>>>>>>> dc692bf (Updated Chat Bot using LLM)
>>>>>>> recovered-work
