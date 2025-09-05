# query_engine.py - Final Clean Version
import os
import time
import json
import subprocess
from dotenv import load_dotenv

import torch
from sentence_transformers import SentenceTransformer, util

try:
    from ollama import Client
except ImportError:
    Client = None
    print("⚠️ Ollama client not installed. Local LLM may not work.")

import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Config ---
EMBEDDINGS_FILE = 'embeddings.pt'
CHUNKS_FILE = 'text_chunks.json'
FAQ_FILE = 'faq.json'
MODEL_NAME = 'all-MiniLM-L6-v2'
LOCAL_LLM_MODEL = 'phi3'
SIMILARITY_THRESHOLD = 0.85

# --- Load Models & Data ---
print("🔄 Loading models and embeddings...")
sbert_model = SentenceTransformer(MODEL_NAME)

try:
    doc_embeddings = torch.load(EMBEDDINGS_FILE)
    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        text_chunks = json.load(f)
except FileNotFoundError:
    print(f"⚠️ '{EMBEDDINGS_FILE}' or '{CHUNKS_FILE}' not found. RAG will not work.")
    doc_embeddings, text_chunks = None, None

# --- Load FAQ & embeddings ---
def load_faq_and_create_embeddings(model):
    if not os.path.exists(FAQ_FILE):
        return [], None
    try:
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            faq_data = json.load(f)
        if not faq_data:
            return [], None
        faq_queries = [item['query'] for item in faq_data]
        faq_embeddings = model.encode(faq_queries, convert_to_tensor=True)
        return faq_data, faq_embeddings
    except Exception:
        return [], None

faq_data, faq_embeddings = load_faq_and_create_embeddings(sbert_model)

# --- Gemini API setup ---
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"⚠️ Error configuring Gemini API: {e}")
else:
    print("⚠️ GEMINI_API_KEY not found. Gemini fallback unavailable.")

# --- Helper Functions ---
def search_faq(query_embedding, faq_embeddings, faq_data):
    if faq_embeddings is None or not faq_data:
        return None
    cosine_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    best_score, best_idx = torch.max(cosine_scores, dim=0)
    return faq_data[best_idx]['answer'] if best_score > SIMILARITY_THRESHOLD else None

def retrieve_relevant_chunks(query, model, embeddings, text_chunks, top_k=5):
    if embeddings is None or text_chunks is None:
        return []
    query_embedding = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = torch.topk(cosine_scores, k=min(top_k, len(text_chunks))).indices.tolist()
    return [text_chunks[idx] for idx in top_indices]

def generate_with_local_llm(query, context):
    """Generates an answer using the local Ollama model with enhanced prompts."""
    system_prompt = """
    You are 'Krishi Mitra', a friendly and helpful agricultural advisor.
    Answer questions based ONLY on the provided context.

    RULES:
    - Do not mention "the text" or "document"; synthesize as your own knowledge.
    - Be friendly and encouraging.
    - If context doesn't have the answer, say "I'm sorry, I couldn't find specific details on that in my resources."
    - Use bullet points for lists.
    """
    try:
        response = ollama.chat(
            model=LOCAL_LLM_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user',
                 'content': f"Context:\n{context}\n\nQuestion:\n{query}"}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Local LLM error: {e}"

def generate_with_gemini_api(query, context):
    """Generates an answer using the Gemini API."""
    if not gemini_model:
        return "Gemini API is not configured."
    prompt = f"""
    You are 'Krishi Mitra', a friendly and knowledgeable agricultural expert in India.
    Answer the question clearly and conversationally, using ONLY the provided context.

    Context:
    {context}

    Question:
    {query}
    """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"

def stop_ollama_server():
    """Stops any running Ollama server process to free system resources."""
    try:
        subprocess.run(["pkill", "-f", "ollama"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
    except FileNotFoundError:
        pass

def update_faq_file(faq_data, query, answer):
    """Appends a new Q&A pair to faq.json."""
    new_entry = {"query": query, "answer": answer}
    faq_data.append(new_entry)
    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(faq_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved new Q&A to '{FAQ_FILE}'.")

# --- Main Query Engine Function ---
def run_query_engine(query: str) -> str:
    global faq_data, faq_embeddings

    query_embedding = sbert_model.encode(query, convert_to_tensor=True)

    # 1. Check FAQ first
    faq_answer = search_faq(query_embedding, faq_embeddings, faq_data)
    if faq_answer:
        return faq_answer

    # 2. Retrieve relevant chunks
    relevant_chunks = retrieve_relevant_chunks(query, sbert_model, doc_embeddings, text_chunks)
    if not relevant_chunks:
        return "I'm sorry, I couldn't find specific details in my knowledge base."

    context_str = "\n---\n".join(relevant_chunks)

    # 3. Generate answer using AI
    try:
        # Force a failure here to test Gemini fallback
        raise ValueError("Simulating local LLM failure for testing.")
        final_answer = generate_with_local_llm(query, context_str)
        if not final_answer or len(final_answer.strip()) < 10:
            raise ValueError("Local LLM returned unhelpful response.")
    except Exception:
        stop_ollama_server()
        final_answer = generate_with_gemini_api(query, context_str)

    # 4. Update FAQ if answer is good
    if "error" not in final_answer.lower() and len(final_answer.split()) > 5:
        update_faq_file(faq_data, query, final_answer)
        faq_data, faq_embeddings = load_faq_and_create_embeddings(sbert_model)

    return final_answer

# --- Interactive Loop ---
def main():
    print(f"\nWelcome! I'm Krishi Mitra, your Agri-Advisor Bot.")
    print(f"I'm using '{LOCAL_LLM_MODEL}' locally, with Gemini as fallback.")
    print("Type your question, or 'exit' to quit.\n")

    while True:
        try:
            query = input("> ").strip()
            if query.lower() == "exit":
                stop_ollama_server()
                break
            if not query:
                continue

            stop_ollama_server()
            print("\n🔎 Searching through resources...")
            answer = run_query_engine(query)
            print("\nAnswer:\n")
            print(answer)
            print("\n" + "="*50 + "\n")

        except KeyboardInterrupt:
            stop_ollama_server()
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
