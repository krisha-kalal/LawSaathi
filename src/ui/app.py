import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="LawSaathi - AI Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/query"

# 2. Sidebar Configuration
st.sidebar.title("⚖️ LawSaathi Dashboard")
st.sidebar.markdown("""
**Domain-Specific Legal RAG Engine**
- **Document**: Constitution of India
- **Retrieval**: BM25 + Vector Hybrid Search
- **Re-Ranker**: Cross-Encoder (`ms-marco`)
- **LLM**: Gemini 3.6 Flash
""")

st.sidebar.divider()
top_candidates = st.sidebar.slider("Top Candidates (Hybrid Retrieval)", 10, 50, 50)
final_top_k = st.sidebar.slider("Final Re-Ranked Chunks (LLM Context)", 1, 15, 12)

if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# 3. Main Chat Title
st.title("LawSaathi: Constitutional Law Assistant")
st.caption("Ask questions about Fundamental Rights, Duties, Articles, and Schedules.")

# 4. Initialize Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I am LawSaathi. How can I assist you with Indian Constitutional Law today?"}
    ]

# 5. Render Existing Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle New User Input
if prompt := st.chat_input("Ask a legal question... (e.g., 'What is Article 21?')"):
    # Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI Backend & Render Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Executing Hybrid Retrieval & Re-Ranking..."):
            try:
                payload = {
                    "question": prompt,
                    "top_candidates": top_candidates,
                    "final_top_k": final_top_k
                }
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    # Display Source Badges
                    if sources:
                        st.markdown("---")
                        st.caption("**Source Citations:**")
                        pages = sorted(list(set(s["page"] for s in sources if s["page"] > 0)))
                        page_badges = " ".join([f"`Page {p}`" for p in pages])
                        st.markdown(f"📍 **Retrieved PDF Context:** {page_badges}")

                    # Append to session history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI backend. Ensure `uvicorn src.api.app:app` is running on port 8000.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")