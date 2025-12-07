import pandas as pd
import os
import json
import datetime
import time
import re  # <--- Added Regex
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
DATA_FILE = "feedback_data.csv"

# GROQ CONFIGURATION
MODEL_NAME = "llama-3.3-70b-versatile" 

def configure_ai():
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None
    
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Timestamp", "Rating", "Review", "AI_Response", "Summary", "Action_Item"])
    return pd.read_csv(DATA_FILE)

def save_entry(rating, review, ai_response, summary, action):
    df = load_data()
    new_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Rating": rating, "Review": review,
        "AI_Response": ai_response, "Summary": summary, "Action_Item": action
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def get_ai_analysis(rating, review):
    client = configure_ai()
    if not client:
        return {"user_reply": "Error: Missing API Key", "summary": "Config Error", "action": "Check .env"}

    prompt = f"""
    You are a Customer Experience AI. Analyze this feedback:
    Rating: {rating}/5 Stars
    Review: "{review}"
    
    Generate strict JSON with exactly these keys: "user_reply", "summary", "action".
    Do not add introductory text.
    """
    
    retries = 0
    max_retries = 3
    
    while retries < max_retries:
        try:
            print(f"🤖 Calling Groq API (Attempt {retries + 1})...")
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful AI. Output strictly in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            raw_text = response.choices[0].message.content.strip()
            
            # Print what the AI actually said
            print(f"👀 RAW RESPONSE: {raw_text}")

            # ROBUST PARSING: Find JSON using Regex (ignores "Here is your JSON" text)
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                clean_json = json_match.group(0)
                return json.loads(clean_json)
            else:
                raise ValueError("No JSON found in response")

        except Exception as e:
            print(f"❌ API Error: {e}")
            time.sleep(2)
            retries += 1

    # Fallback
    print("⚠️ Max retries reached. Using fallback.")
    return {
        "user_reply": "Thank you for your feedback! (System busy)",
        "summary": "Manual Review Required",
        "action": "Check Server Logs"
    }