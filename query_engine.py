<<<<<<< HEAD
# query_engine.py (Final Version with Enhanced Personality and Prompts)
import torch
from sentence_transformers import SentenceTransformer, util
import json
import ollama
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# --- Config ---
=======
import torch
from sentence_transformers import SentenceTransformer, util
import json
import os
import subprocess
from dotenv import load_dotenv

# Correct Ollama import
try:
    from ollama import Client
except ImportError:
    Client = None
    print("⚠️ Ollama client not installed. Falling back to Gemini only.")

import google.generativeai as genai

# --- Config ---
load_dotenv()
>>>>>>> recovered-work
EMBEDDINGS_FILE = 'embeddings.pt'
CHUNKS_FILE = 'text_chunks.json'
MODEL_NAME = 'all-MiniLM-L6-v2'
LOCAL_LLM_MODEL = 'phi3'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
<<<<<<< HEAD

# Configure the Gemini API client
=======
FAQ_FILE = 'faq.json'
SIMILARITY_THRESHOLD = 0.85

# --- Setup Models & Data (loaded once at startup) ---
print("🔄 Loading sentence transformer models and embeddings...")
sbert_model = SentenceTransformer(MODEL_NAME)

# Load document embeddings and chunks
try:
    doc_embeddings = torch.load(EMBEDDINGS_FILE)
    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        text_chunks = json.load(f)
except FileNotFoundError:
    print(f"⚠️ WARNING: '{EMBEDDINGS_FILE}' or '{CHUNKS_FILE}' not found. RAG will not work.")
    print("   Please run the 'ingest_engine.py' script first.")
    doc_embeddings, text_chunks = None, None


# Load FAQ data and embeddings
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
print("✅ Models and embeddings loaded.")

# Gemini setup
>>>>>>> recovered-work
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
<<<<<<< HEAD
        print(f"Error configuring Gemini API: {e}")
else:
    print("Warning: GEMINI_API_KEY not found. Fallback will not be available.")


def retrieve_relevant_chunks(query, model, embeddings, text_chunks, top_k=5):
    """Finds the most relevant text chunks."""
=======
        print(f"⚠️ Error configuring Gemini API: {e}")


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
>>>>>>> recovered-work
    query_embedding = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = torch.topk(cosine_scores, k=min(top_k, len(text_chunks))).indices.tolist()
    return [text_chunks[idx] for idx in top_indices]


<<<<<<< HEAD
def generate_with_local_llm(query, context):
    """Generates an answer using the local Ollama model with an enhanced prompt."""
    # This prompt gives the local model a clear personality and rules.
    system_prompt = """
    You are 'Krishi Mitra', a friendly and helpful agricultural advisor.
    Your goal is to answer questions in a conversational way based ONLY on the provided context.

    **RULES:**
    - **DO NOT** mention "the text" or "the document". Synthesize the information as your own knowledge.
    - Be friendly and encouraging.
    - If the context doesn't have the answer, say "I'm sorry, I couldn't find specific details on that in my resources."
    - Use bullet points for lists.
    """
    try:
        response = ollama.chat(
            model=LOCAL_LLM_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user',
                 'content': f"Here is the context I have:\n{context}\n\nBased on that, please answer this question: {query}"}
            ]
        )
        return response['message']['content']
    except Exception as e:
        raise e


def generate_with_gemini_api(query, context):
    """Generates an answer using the Gemini API with a more detailed personality prompt."""
    if not gemini_model:
        return "Gemini API is not configured. Please check your API key."

    # This more detailed prompt plays to the strengths of a powerful cloud model like Gemini.
    prompt = f"""
    You are 'Krishi Mitra', a friendly and knowledgeable agricultural expert based in India. Your goal is to help farmers by answering their questions in a clear, encouraging, and conversational way.

    **Your Strict Instructions:**
    1.  **Synthesize, Don't Quote:** Read the context I provide below and use it to form your own expert answer. **Never** say things like "According to the document..." or "The text states...". You must speak as if you know this information yourself.
    2.  **Be Conversational:** Use a friendly and helpful tone. For example, instead of "The recommended dose is...", say "For your crops, you'll want to use...".
    3.  **Stay Grounded in the Text:** Base your entire answer *only* on the provided context. Do not use any outside knowledge, even if you know it.
    4.  **Handle Missing Information Gracefully:** If the context doesn't have the answer, say something friendly and clear, like, "That's a great question! I looked through my resources but couldn't find specific information on that topic for you."
    5.  **Format for Clarity:** If you are listing things like crop varieties, steps, or recommendations, please use bullet points to make the information easy to read.

    ---
    **CONTEXT FROM MY BOOKS:**
    {context}
    ---

    **FARMER'S QUESTION:**
    {query}
    """
    try:
        print("✅ Calling Gemini API...")
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error with Gemini API call: {e}"


def stop_ollama_server():
    """Stops any running Ollama server process to free up system resources."""
    try:
        subprocess.run(["pkill", "-f", "ollama"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("🛑 Ollama server process stopped to ensure stability.")
        time.sleep(2)
    except FileNotFoundError:
        pass


def main():
    try:
        print("Loading pre-computed data...")
        model = SentenceTransformer(MODEL_NAME)
        embeddings = torch.load(EMBEDDINGS_FILE)
        with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
            text_chunks = json.load(f)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("Error: Missing embeddings or chunks file. Run ingest_data.py first.")
        return

    print(f"\nWelcome! I'm Krishi Mitra, your Agri-Advisor Bot.")
    print(f"I'm using '{LOCAL_LLM_MODEL}' locally, with Gemini as a fallback.")
    print("Ask me a question, or type 'exit' to quit.")

    while True:
        query = input("> ").strip()
        if query.lower() == "exit":
            stop_ollama_server()
            break
        if not query:
            continue

        stop_ollama_server()

        print("\n🔎 Looking through my resources...")
        relevant_chunks = retrieve_relevant_chunks(query, model, embeddings, text_chunks)

        if not relevant_chunks:
            print(
                "\nAnswer:\nThat's a great question! I looked through my resources but couldn't find specific information on that topic for you.")
            print("\n" + "=" * 50 + "\n")
            continue

        context_str = "\n---\n".join(relevant_chunks)
        final_answer = ""

        try:
            print(f"💡 Thinking with my local brain ({LOCAL_LLM_MODEL})... (Timeout: 20s)")
            final_answer = generate_with_local_llm(query, context_str)
            if not final_answer or len(final_answer.strip()) < 10:
                raise ValueError("Local model returned an unhelpful response.")
            print("✅ Got it!")

        except Exception as e:
            print(f"⏳ My local brain is taking a bit long... Reason: {e}")
            stop_ollama_server()
            print("💡 Switching to my cloud brain (Gemini API) for a faster answer...")
            final_answer = generate_with_gemini_api(query, context_str)

        print("\nAnswer:\n")
        print(final_answer)
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()
=======
def generate_with_gemini_api(query, context):
    if not gemini_model:
        return "Gemini API is not configured. Please add GEMINI_API_KEY to your .env file."
    try:
        prompt = f"You are Krishi Mitra, an expert agricultural assistant. Answer the user's question clearly and practically, like you are advising a farmer. Use only the provided context.\n\nContext:\n{context}\n\nQuestion:\n{query}"
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred with the Gemini API: {e}"


def update_faq_file(faq_data, query, answer):
    """Appends a new question-answer pair to the faq.json file."""
    new_entry = {"query": query, "answer": answer}
    faq_data.append(new_entry)
    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(faq_data, f, indent=2, ensure_ascii=False)
    print(f"✅ New Q&A pair saved to '{FAQ_FILE}'.")


# --- Main Query Engine Function ---
def run_query_engine(query: str) -> str:
    # --- FIX: Moved global declarations to the top of the function ---
    global faq_data, faq_embeddings

    query_embedding = sbert_model.encode(query, convert_to_tensor=True)

    # 1. Check FAQ first for a quick answer
    faq_answer = search_faq(query_embedding, faq_embeddings, faq_data)
    if faq_answer:
        return faq_answer

    # 2. If not in FAQ, search documents and use LLM
    relevant_chunks = retrieve_relevant_chunks(query, sbert_model, doc_embeddings, text_chunks)
    if not relevant_chunks:
        return "I'm sorry, I couldn't find specific details about that in my knowledge base."

    context_str = "\n---\n".join(relevant_chunks)

    # 3. Generate a new answer using the AI
    final_answer = generate_with_gemini_api(query, context_str)

    # 4. Save the new answer to the FAQ, but only if it's a good quality answer
    if "error" not in final_answer.lower() and len(final_answer.split()) > 5:
        update_faq_file(faq_data, query, final_answer)
        # Reload the FAQ embeddings to include the new question
        faq_data, faq_embeddings = load_faq_and_create_embeddings(sbert_model)
    else:
        print("⚠️ AI-generated answer was not saved to FAQ due to low quality or error.")

    return final_answer

>>>>>>> recovered-work
