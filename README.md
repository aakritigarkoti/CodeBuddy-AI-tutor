# 🤖 CodeBuddy - Your AI Coding Companion

**CodeBuddy** is an intelligent, multi-modal AI agent designed to make technical learning more interactive, visual, and intuitive. Built using **Streamlit** and powered by **Google Gemini**, it serves as your 24/7 personal coding tutor — explaining complex topics through a combination of **text, examples, and diagrams**.

---

## 📚 Project Overview

Learning to code can be overwhelming — especially when online resources are either too vague or too complex. **CodeBuddy** solves this by offering structured answers broken into **4 major parts**:

1. **Concise Concept Summary**
2. **Real-world Example**
3. **Diagram/Visual Representation**
4. **Clean Code Snippet**

This format ensures deep conceptual clarity for both beginners and intermediates.

This project was developed as part of the **DT Fellowship Simulation** under the "Build Your Own AI Agent" challenge.

---

## 🚀 Features

✅ **Smart Prompt Analysis:** Understands user’s coding-related query and decides how to respond effectively.

✅ **Structured Answers in 4 Parts:** Auto-generates:
- Concept summary
- Real-world analogy
- Diagram or image
- Code snippet

✅ **Diagram Support with MermaidJS:** Explains logic visually using flowcharts and diagrams.

✅ **Image Search using Pexels API:** Instead of generating, CodeBuddy smartly searches high-quality free images related to the concept.

✅ **Session Memory:** Keeps track of conversation using `st.session_state`.

✅ **Export to PDF:** Users can export the latest answer for revision or notes.

✅ **Clean & Responsive UI:** Streamlit-based interface with clear chat layout and sidebar instructions.

---

## 🛠️ Tech Stack

| Component         | Description                                   |
|------------------|-----------------------------------------------|
| **Frontend**      | Streamlit                                     |
| **Language**      | Python                                        |
| **Core LLM**      | Google Gemini 1.5 Flash                       |
| **APIs Used**     | Google GenerativeAI, Pexels API               |
| **PDF Export**    | `markdown2`, `xhtml2pdf`                      |
| **Diagram Support** | MermaidJS (Markdown rendering)             |

---

## 🧪 Development Journey & Challenges Faced

Building CodeBuddy was not just coding — it was about solving **real developer problems** under resource and time constraints. Here's a breakdown:

---

### 🔁 Pivoting from OpenAI to Gemini

**Initial Plan:** We started with OpenAI (GPT-4) for high-quality responses.

**Challenge:** It required a paid subscription and strict API quotas, which was not suitable for a free, student-level assignment.

**Solution:** Switched to **Google Gemini**, which provides a generous free tier and excellent multimodal support. The transition involved:

- Rewriting prompts for Gemini
- Adapting input/output formatting
- Testing Gemini's capabilities for educational content

---

### 🖼️ Diagram & Visual Explanation – 3 Attempts

Our goal was to **include visuals** for every concept. This took **3 iterations**:

#### 1. MermaidJS Diagrams (✅ Finalized)
- Used for flowcharts and logic-based topics (e.g., recursion, loops).
- Required correct Markdown formatting (` ```mermaid `).
- Gemini was guided to generate diagram code in proper syntax.

#### 2. AI Image Generation with Imagen (❌ Dropped)
- Tried using Google’s **Imagen model** via Vertex AI.
- Worked well for generating custom diagrams.
- But needed a **billing-enabled GCP account**, which conflicted with our goal of making the app free and simple for everyone.

#### 3. Smart Image Search (✅ Final Choice)
- Gemini generates a **smart image search prompt** (like “stack vs heap memory diagram”) which we feed to **Pexels API**.
- The images are relevant and legally free.
- Perfect balance between visual clarity and accessibility.

---

### 🎤 Voice Input Attempt (❌ Dropped)

**Idea:** Make the app more accessible with voice-to-text input using:

- `SpeechRecognition`, `streamlit-mic-recorder`, `pydub`

**Problem:** These required `FFmpeg` installation and setting PATH manually, especially hard on Windows.

**Decision:** We dropped the voice feature to **keep setup simple**, avoiding any external tools.

---

## 💡 Design Philosophy

- **100% Free:** Every tool and API used is free and open-source.
- **Minimal Setup:** No system-level dependencies. Just clone and run.
- **Multi-modal Learning:** Text + Visuals + Code = Deep Understanding
- **Beginner Friendly:** Clean UI and well-structured responses.

---

## 📥 Setup Instructions

1. **Clone the Repo**
```bash
git clone https://github.com/your-username/codebuddy.git
cd codebuddy
Install Requirements

bash
Copy
Edit
pip install -r requirements.txt
Set Your API Keys
Create a .env file:

ini
Copy
Edit
GOOGLE_API_KEY=your_google_api_key
PEXELS_API_KEY=your_pexels_api_key
Run the App

bash
Copy
Edit
streamlit run app.py

📸 Screenshots
(Add screenshots showing: a chat, diagram, image, and export button. This boosts judge appeal.)

🙏 Acknowledgments
Developed as part of DT Fellowship Simulation

Core AI by Google Gemini

Image results from Pexels API

Diagram support via MermaidJS

✨ Future Improvements
Voice-to-text via streamlit-mic-recorder with proper FFmpeg config

User authentication with login-based history saving

Option to rate each answer for further tuning

