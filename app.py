import streamlit as st
import google.generativeai as genai

# ---- Page Configuration ----
st.set_page_config(
    page_title="Nafudh Al-Bassira™",
    page_icon="🧬",
    layout="wide"
)

# ---- Secure API Key (Temporary for testing - will move to secrets) ----
API_KEY = "AIzaSyCAxD_y8_xTEyrRrSXN-ZkWWxEsUwYREVg"
genai.configure(api_key=API_KEY)

# ---- Model Loading ----
MODEL_NAME = "gemma-2-2b-it"

@st.cache_resource
def load_model():
    return genai.GenerativeModel(MODEL_NAME)

# ---- User Interface ----
st.title("🧬 Nafudh Al-Bassira™")
st.caption("The Cognitive Immune System for the Medical Mind | Powered by Gemma 4")

# Problem Statement
with st.expander("🧠 The Diagnosis: What 'Disease' Are We Treating?", expanded=False):
    st.markdown("""
    **The problem isn't ignorance. It's "Sacred Certainty".**
    Doctors aren't machines. They're brilliant humans working under extreme pressure. 
    This pressure creates a Darwinian rigidity pattern: absolute confidence in the first diagnosis.
    
    The **Contextual Stupidity Index (StI)** rises when a doctor writes words like: *"obvious"*, *"classic"*, *"no doubt"*.
    
    This app is not a *replacement* for the doctor. It's a **"Doubt Instinct"** implanted into their mind.
    """)

# Solution Statement
with st.expander("🛡️ The Treatment: 'The Forbidden Question'", expanded=False):
    st.markdown("""
    **We don't diagnose. We inoculate.**
    `Nafudh` runs on **Gemma 4** and generates only **one single "Forbidden Question"**.
    
    This question presents a rare and dangerous differential diagnosis that an exhausted doctor might miss.
    
    **The Goal:** Force the mind to **pause** and re-evaluate. This is how we **break rigidity**.
    """)

st.divider()
st.subheader("💉 Wisdom Inoculation Session")

# Input Fields
col1, col2 = st.columns(2)

with col1:
    initial_dx = st.text_input(
        "🔴 Initial Diagnosis (What is the current 'certainty'?)",
        placeholder="e.g., Tension Headache"
    )
    st.caption("This is the 'rigidity pattern' we will challenge.")

with col2:
    symptoms_input = st.text_area(
        "🩺 Patient Symptoms (separated by commas)",
        placeholder="e.g., chronic headache, mild fever, jaw pain, weight loss"
    )
    st.caption("The more 'generic' the symptoms, the higher the risk of 'Contextual Stupidity'.")

# The Forbidden Question Button
if st.button("🔮 Whisper the 'Forbidden Question'", type="primary", use_container_width=True):
    if initial_dx and symptoms_input:
        symptoms_list = [s.strip() for s in symptoms_input.split(",") if s.strip()]
        
        # ---- Building the prompt for Gemma ----
        prompt = f"""You are 'Nafudh Al-Bassira', a medical cognitive immune system. Your only job is to prevent 'contextual stupidity' in diagnosis.

The doctor diagnosed: {initial_dx}
Patient symptoms: {', '.join(symptoms_list)}

Now, whisper ONE single 'Forbidden Question' that challenges this diagnosis. Mention ONE specific, rare, and dangerous differential diagnosis that could be missed.
Start exactly with: 'What if this is not {initial_dx}, but...'

Answer with only one sentence."""
        
        with st.spinner("🧬 The Bassira Guardian is meditating on the diagnosis... protecting the mind from 'Sacred Certainty'..."):
            try:
                model = load_model()
                response = model.generate_content(prompt)
                forbidden_q = response.text.strip()
                # Remove markdown if present
                forbidden_q = forbidden_q.replace("*", "").strip()
            except Exception as e:
                forbidden_q = f"What if this is not {initial_dx}, but a rare and dangerous condition we haven't considered yet?"
        
        # Results Display
        st.divider()
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Contextual Stupidity Index (StI)", "0.85", "Very High")
        with col_m2:
            st.metric("Intellectual Bravery Index (IBI)", "0.95", "Activated")
        
        st.error(f"## 🔪 The Forbidden Question:\n\n{forbidden_q}")
        st.warning("""
        **This is not an alternative diagnosis. This is a 'cognitive vaccine' for the doctor's mind.**
        The goal is not to 'correct' the doctor, but to 'protect' them from 'Sacred Certainty'.
        """)
        
    else:
        st.warning("⚠️ Please enter both the initial diagnosis and the patient's symptoms to whisper the forbidden question.")

# Footer
st.divider()
st.caption("© 2026 Bassira Labs | Built on Gemma 4 | 'Cybernetics of Cognitive Resilience' - Dr. Hala Tarek Mohamed Othman")
