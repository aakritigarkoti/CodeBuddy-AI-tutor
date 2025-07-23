import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from io import BytesIO
from xhtml2pdf import pisa
import markdown2

# --- FUNCTION TO CONVERT MARKDOWN TO PDF ---
def convert_to_pdf(markdown_text):
    """Converts a Markdown string to a PDF file in memory."""
    html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks"])
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf_buffer)
    if pisa_status.err:
        return None
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# --- FUNCTION TO SEARCH FOR IMAGES WITH PEXELS ---
def get_image_url(query, pexels_api_key):
    """Searches for an image on Pexels and returns the URL."""
    headers = {"Authorization": pexels_api_key}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}
    url = "https://api.pexels.com/v1/search"
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["large"]
    except requests.exceptions.RequestException as e:
        st.error(f"Pexels API Error: {e}")
    return None

# --- FUNCTION TO PROCESS A PROMPT ---
def process_prompt(prompt_text):
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and searching... 🖼️"):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                full_prompt = f"""
                You are CodeBuddy, an expert AI coding tutor for a user who needs to understand: "{prompt_text}".

                First, decide if an image would help. If so, create a detailed search query using the tag [SEARCH_IMAGE: ...].
                Example: [SEARCH_IMAGE: simple photosynthesis diagram for kids illustration]

                Then, continue with the normal 4-section explanation. If a text-diagram is better, use Mermaid.

                ### 🧠 Concept Summary
                ### 🔍 Real World Example
                ### 📊 Visualization (Code or Diagram)
                ### 🎯 Quick Quiz
                """
                response = model.generate_content(full_prompt)
                response_text = response.text
                st.session_state.last_response = response_text
                
                if "[SEARCH_IMAGE:" in response_text:
                    start_tag = "[SEARCH_IMAGE:"
                    end_tag = "]"
                    start_index = response_text.find(start_tag) + len(start_tag)
                    end_index = response_text.find(end_tag, start_index)
                    search_query = response_text[start_index:end_index].strip()
                    response_text = response_text.replace(f"[SEARCH_IMAGE:{search_query}]", "")
                    image_url = get_image_url(search_query, pexels_api_key)
                    if image_url:
                        st.image(image_url, caption=f"Image for: {search_query}")
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                error_message = f"An error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# --- API AND MODEL CONFIGURATION ---
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
pexels_api_key = os.getenv("PEXELS_API_KEY")

if google_api_key:
    genai.configure(api_key=google_api_key)
else:
    st.error("Google API key not found. Please check your .env file.")

st.title("🤖 CodeBuddy - Your AI Coding Tutor")
st.markdown("Your friendly AI-powered tutor for mastering any coding concept!")
st.markdown("---")


# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛠️ Export & Info")
    if st.session_state.last_response:
        pdf_data = convert_to_pdf(st.session_state.last_response)
        if pdf_data:
            st.download_button(
                label="📄 Export Last Answer as PDF",
                data=pdf_data,
                file_name="CodeBuddy_Answer.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Ask a question to generate an answer you can export.")
    
    st.markdown("---") 
    with st.expander("ℹ️ About CodeBuddy"):
        st.markdown("""
        **Creator:** [Your Name Here]
        
        **Assignment:** DT Fellowship Simulation - AI Agent
        
        **Purpose:** To build a simple, helpful AI agent using a multi-step architecture and to practice iterating with AI tools.
        
        ---
        
        #### Tools Used:
        - **Language:** Python
        - **Framework:** Streamlit
        - **Core AI:** Google Gemini 1.5 Flash
        - **Image Search:** Pexels API
        - **PDF Export:** xhtml2pdf & markdown2
        """)


# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- NEW: SUGGESTION BUTTONS FOR NEW CHATS ---
if not st.session_state.messages:
    st.info("Get started by asking a question below or trying one of these suggestions!")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Explain what a 'dictionary' is in Python"):
            process_prompt("Explain what a 'dictionary' is in Python")
    
    with col2:
        if st.button("What are SQL Joins?"):
            process_prompt("What are SQL Joins?")
            
    with col3:
        if st.button("Explain recursion with an example"):
            process_prompt("Explain recursion with an example")


# --- TEXT INPUT ---
if prompt := st.chat_input("Ask me any coding topic you're stuck on:"):
    process_prompt(prompt)