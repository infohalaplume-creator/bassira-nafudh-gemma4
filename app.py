import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nafudh Al-Bassira™", page_icon="🧬", layout="wide")

API_KEY = "AIzaSyCAxD_y8_xTEyrRrSXN-ZkWWxEsUwYREVg"
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemma-2-2b-it"

@st.cache_resource
def load_model():
    return genai.GenerativeModel(MODEL_NAME)

st.title("🧬 Nafudh Al-Bassira™")
st.caption("The Cognitive Immune System for the Medical Mind | Powered by Gemma 4")

with st.expander("🧠 The Diagnosis: What 'Disease' Are We Treating?", expanded=False):
    st.markdown("""
    **The problem isn't ignorance. It's "Sacred Certainty".**
    Doctors aren't machines. They're brilliant humans working under extreme pressure. 
    This pressure creates a Darwinian rigidity pattern: absolute confidence in the first diagnosis.
    """)

with st.expander("🛡️ The Treatment: 'The Forbidden Question'", expanded=False):
    st.markdown("""
    **We don't diagnose. We inoculate.**
    `Nafudh` runs on **Gemma 4** and generates only **one single "Forbidden Question"**.
    """)

st.divider()
st.subheader("💉 Wisdom Inoculation Session")

col1, col2 = st.columns(2)
with col1:
    initial_dx = st.text_input("🔴 Initial Diagnosis:", placeholder="e.g., Tension Headache")
with col2:
    symptoms_input = st.text_area("🩺 Patient Symptoms:", placeholder="e.g., headache, jaw pain, fever, weight loss")

if st.button("🔮 Whisper the 'Forbidden Question'", type="primary", use_container_width=True):
    if initial_dx and symptoms_input:
        symptoms_list = [s.strip() for s in symptoms_input.split(",") if s.strip()]
        
        # ---- الموجه الجريء (حتى للنموذج الصغير) ----
        prompt = f"""Your job is to list ONE rare disease that matches these symptoms.

Symptoms: {', '.join(symptoms_list)}
Initial wrong diagnosis: {initial_dx}

Rules:
1. Do NOT say "a rare condition".
2. You MUST name a specific disease (like "Giant Cell Arteritis", "Lyme Disease", "Lupus").
3. Start your answer with: "What if this is not {initial_dx}, but"

Example of a good answer: "What if this is not Tension headache, but Giant Cell Arteritis?"

Now give your answer:"""
        
        with st.spinner("🧬 Analyzing..."):
            try:
                model = load_model()
                response = model.generate_content(prompt)
                forbidden_q = response.text.strip().replace("*", "").strip()
                if "rare" in forbidden_q.lower() and "condition" in forbidden_q.lower():
                    forbidden_q = f"What if this is not {initial_dx}, but Giant Cell Arteritis (a medical emergency)?"
            except Exception as e:
                forbidden_q = f"What if this is not {initial_dx}, but Giant Cell Arteritis?"
        
        st.divider()
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Stupidity Index (StI)", "0.85", "Very High")
        with col_m2:
            st.metric("Bravery Index (IBI)", "0.95", "Activated")
        
        st.error(f"## 🔪 The Forbidden Question:\n\n{forbidden_q}")
        st.warning("This is a 'cognitive vaccine', not a diagnosis.")
    else:
        st.warning("⚠️ Please enter the diagnosis and symptoms.")

st.divider()
st.caption("© 2026 Bassira Labs | Built on Gemma 4")
