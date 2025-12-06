import pandas as pd
import google.generativeai as genai
import os
import json
import datetime
import streamlit as st
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
DATA_FILE = "feedback_data.csv"

# Configure AI
def configure_ai():
    # Try getting key from Streamlit Secrets (Cloud) or .env (Local)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return False
    
    genai.configure(api_key=api_key)
    return True

# Initialize Model
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- DATA FUNCTIONS ---
def load_data():
    """Loads reviews from CSV. Creates file if missing."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=[
            "Timestamp", "Rating", "Review", 
            "AI_Response", "Summary", "Action_Item"
        ])
    return pd.read_csv(DATA_FILE)

def save_entry(rating, review, ai_response, summary, action):
    """Saves a new entry to the CSV file."""
    df = load_data()
    new_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Rating": rating,
        "Review": review,
        "AI_Response": ai_response,
        "Summary": summary,
        "Action_Item": action
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- AI FUNCTIONS ---
def get_ai_analysis(rating, review):
    """
    Generates User Reply, Summary, and Action Item in one shot.
    """
    prompt = f"""
    You are a Customer Experience AI. Analyze this customer feedback:
    Rating: {rating}/5 Stars
    Review: "{review}"

    Generate a JSON response with exactly these keys:
    1. "user_reply": A polite, empathetic response to the customer (max 2 sentences).
    2. "summary": A concise 5-word summary of the issue/praise.
    3. "action": A specific recommended action for the business team.

    Output STRICT JSON.
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception:
        # Fallback if AI fails
        return {
            "user_reply": "Thank you for your feedback!",
            "summary": "Processing Error",
            "action": "Check System Logs"
        }