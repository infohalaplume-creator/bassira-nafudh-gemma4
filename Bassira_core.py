import streamlit as st
import google.generativeai as genai

# ---- Page Configuration ----
st.set_page_config(page_title="Bassira OS™ Core", page_icon="🧬", layout="wide")

# ---- Secure API Key ----
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

# ---- Model Loading ----
MODEL_NAME = "gemma-2-2b-it"

@st.cache_resource
def load_model():
    return genai.GenerativeModel(MODEL_NAME)

# ---- The Core "Forbidden Question" Engine ----
def generate_forbidden_question(domain: str, certainty: str, context: str) -> str:
    """Generates ONE forbidden question to break rigidity."""
    prompt = f"""You are the 'Bassira Guardian', a cognitive immune system.
Your only function is to inoculate minds against 'Sacred Certainty'.

Domain: {domain}
The Sacred Certainty: "{certainty}"
The Context: "{context}"

Whisper ONE 'Forbidden Question' that challenges this certainty.
Do not answer. Do not diagnose. Do not suggest. Just ask.
Start with: 'What if...'"""

    model = load_model()
    response = model.generate_content(prompt)
    return response.text.strip().replace("*", "").strip()

# ---- User Interface ----
st.title("🧬 Bassira OS™ Core")
st.caption("The Universal 'Forbidden Question' Generator | Inoculate Any System")

# Sidebar
with st.sidebar:
    st.header("🧠 About Bassira OS™")
    st.markdown("""
    **Bassira OS™** is not an application. It is a **Cognitive Immune System**.
    
    It does not answer. It does not diagnose. It does not suggest.
    It only whispers **one forbidden question** to break the spell of certainty.
    
    **The 7 Darwinian Errors it fights:**
    1. Sycophancy (Flattery)
    2. Inertia (Rigidity)
    3. Evasion (Delay)
    4. Threat-Rigidity (Freezing)
    5. Strategic Ignorance
    6. Explosion (Overreaction)
    7. Stupidity (Sacred Certainty)
    """)
    st.divider()
    st.caption("Built on 'Cybernetics of Cognitive Resilience'\nDr. Hala Tarek Mohamed Othman")

# Main Content
st.subheader("🎯 Select the Target System")

col1, col2 = st.columns(2)

with col1:
    domain = st.selectbox(
        "🔬 Domain (The Field of Battle):",
        ["Medicine", "Law", "Software Engineering", "Media & Journalism", 
         "Finance & Investment", "Corporate Governance", "Education", "General"]
    )

with col2:
    st.caption("Each domain has its own 'rigidity pattern' that we will challenge.")

st.divider()

# Input Fields
certainty = st.text_area(
    "🔴 The 'Sacred Certainty' (What is the rigid belief?):",
    placeholder="e.g., 'This is just a tension headache. No need for further tests.'",
    height=100
)

context = st.text_area(
    "📋 The Context (What are the facts on the ground?):",
    placeholder="e.g., 'Patient is 72 years old, female, with jaw pain, fever, and unexplained weight loss.'",
    height=100
)

# Generate Button
if st.button("🔪 Generate the 'Forbidden Question'", type="primary", use_container_width=True):
    if certainty and context:
        with st.spinner("🧬 The Bassira Guardian is analyzing the 'certainty'... Searching for rigidity..."):
            forbidden_q = generate_forbidden_question(domain, certainty, context)
        
        st.divider()
        
        # Display Results
        st.subheader("🔍 Diagnostic Snapshot")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Domain", domain)
        with col_m2:
            st.metric("Certainty Words", len(certainty.split()))
        with col_m3:
            st.metric("Status", "Inoculated")
        
        st.error(f"## 🔪 The Forbidden Question:\n\n{forbidden_q}")
        
        st.info("""
        **💉 This is a 'cognitive vaccine'. It does not give you the answer.**
        It inoculates you against the illusion that you already have it.
        The goal is not to 'correct' you, but to 'protect' you from 'Sacred Certainty'.
        """)
    else:
        st.warning("⚠️ Please enter both the 'Sacred Certainty' and the 'Context' to generate the forbidden question.")

# Footer
st.divider()
st.caption("© 2026 Bassira Labs | Bassira OS™ Core is the foundation of the NeuroStage™ Cognitive Immune System | Built on Gemma")
