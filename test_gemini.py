# test_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

print("Attempting to load API key from .env file...")

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("\n❌ ERROR: Could not find GEMINI_API_KEY in your .env file.")
    print("   Please ensure the .env file exists and the key name is correct.")
else:
    print("✅ Found API key in .env file.")
    try:
        print("\nConfiguring Gemini API...")
        genai.configure(api_key=GEMINI_API_KEY)

        print("Initializing Gemini model...")
        model = genai.GenerativeModel('gemini-1.5-flash')

        print("Sending a test message to Gemini...")
        response = model.generate_content("Hello, world!")

        print("\n🎉 SUCCESS! The Gemini API is working correctly.")
        print("   Test response:", response.text)

    except Exception as e:
        print(f"\n❌ ERROR: An error occurred while testing the Gemini API.")
        print(f"   Error details: {e}")

        # I am a farmer with sandy loam soil. What are some suitable crops I can grow?