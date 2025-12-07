import pandas as pd
import os
import json
import datetime
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# load the env variable
load_dotenv()
DATA_FILE = "feedback_data.csv"

# load the model 
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
    Generate strict JSON with keys: "user_reply", "summary", "action".
    """
    
    while True: # Infinite retry loop 
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful AI. Output strictly in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            raw_text = response.choices[0].message.content.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "")
            return json.loads(raw_text)

        except Exception as e:
            # cooling down period before retrying
            time.sleep(5)