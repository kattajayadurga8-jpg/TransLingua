import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="TransLingua AI", page_icon="🌐", layout="wide")

st.title("🌐 TransLingua: AI-Powered Multi-Language Translator")
st.markdown("---")

if not api_key:
    st.error("❌ API Key missing. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

with st.sidebar:
    st.header("Project Settings")
    
    scenario = st.selectbox(
        "Select Scenario", 
        ["General", "Scenario 1: Global Business", "Scenario 2: Academic Research", "Scenario 3: Travel Assistance"]
    )
    
    source_lang = st.selectbox("Source Language", ["English", "Telugu", "Hindi", "French", "Spanish", "German"])
    target_lang = st.selectbox("Target Language", ["Hindi", "Telugu", "English", "French", "Spanish", "German"])
    
    st.info(f"Current Mode: {scenario}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Text")
    user_input = st.text_area("Enter text to translate:", placeholder="Type or paste your content here...", height=250)

def get_system_instruction(mode):
    if "Business" in mode:
        return "You are a professional business translator. Focus on corporate tone, marketing consistency, and technical accuracy for global expansion."
    elif "Academic" in mode:
        return "You are a scholarly translator. Use formal, academic vocabulary suitable for research papers and international peer-reviewed journals."
    elif "Travel" in mode:
        return "You are a travel assistant. Provide simple, clear, and practical translations for signs, menus, and local interactions."
    return "You are a helpful, accurate language translator."

if st.button("🚀 Translate with AI"):
    if user_input.strip():
        with st.spinner("Analyzing and Translating..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=get_system_instruction(scenario),
                        temperature=0.3, 
                    ),
                    contents=f"Translate the following text from {source_lang} to {target_lang}: {user_input}"
                )
                
                with col2:
                    st.subheader("Translation Result")
                    st.success(response.text)
                    st.download_button("📥 Download Translation", response.text, file_name="translation.txt")
                    
            except Exception as e:
                st.error(f"AI Service Error: {e}")
    else:
        st.warning("Please enter text before clicking translate.")

st.markdown("---")
st.caption("Developed for APSCHE SmartInternz | Cloud Application Development Project")
