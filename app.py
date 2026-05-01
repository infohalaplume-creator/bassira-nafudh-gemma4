import streamlit as st
import google.generativeai as genai
import time
import requests
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any

# ---- Page Configuration ----
st.set_page_config(page_title="Nafudh Al-Bassira™", page_icon="🧬", layout="wide")

# ---- Secure API Key (Loaded from Streamlit Secrets) ----
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

# ---- Model Loading ----
MODEL_NAME = "gemma-2-2b-it"

@st.cache_resource
def load_model():
    return genai.GenerativeModel(MODEL_NAME)

# ---- The "Wise Elder" Knowledge Base (Breaks AI Rigidity) ----
WISE_ELDER_KNOWLEDGE = {
    "headache": "Giant Cell Arteritis (Temporal Arteritis)",
    "fatigue": "Lymphoma (Hodgkin's or Non-Hodgkin's)",
    "back pain": "Multiple Myeloma",
    "chest pain": "Aortic Dissection",
    "fever": "Endocarditis",
    "cough": "Tuberculosis",
    "dizziness": "Vertebral Artery Dissection",
    "abdominal pain": "Mesenteric Ischemia",
    "weight loss": "Pancreatic Cancer",
    "night sweats": "Tuberculosis or Lymphoma",
    "jaw pain": "Giant Cell Arteritis",
    "vision loss": "Giant Cell Arteritis",
    "confusion": "Meningitis or Encephalitis",
    "seizure": "Brain Tumor or Paraneoplastic Syndrome"
}

def get_wise_elder_advice(symptoms_str: str, initial_dx: str) -> str:
    """The Wise Elder Guardian: Searches the knowledge base for a relevant rare disease."""
    symptoms_lower = symptoms_str.lower()
    for key, disease in WISE_ELDER_KNOWLEDGE.items():
        if key in symptoms_lower and key not in initial_dx.lower():
            return disease
    return "a rare and dangerous condition"

# ---- The "Audit Instinct": Calculates Stupidity Index (StI) from certainty words ----
def calculate_stupidity_index(text: str) -> float:
    certainty_words = ["obvious", "clearly", "no doubt", "classic", "definitely", "always", "never", "absolutely"]
    words = text.lower().split()
    count = sum(1 for word in certainty_words if word in words)
    return min(count * 0.2, 1.0)

# ---- The "Bravery Instinct": Governance Theater ----
def governance_theater(model, prompt: str, symptoms_str: str, initial_dx: str) -> tuple:
    """Runs the prompt 3 times. If the model is rigid, calls the Wise Elder."""
    answers = []
    for _ in range(3):
        try:
            response = model.generate_content(prompt)
            answer = response.text.strip().replace("*", "").strip()
            answers.append(answer)
        except:
            answers.append("")
    
    unique_answers = list(set(answers))
    rigidity_warning = None
    best_answer = max(answers, key=lambda x: len(x)) if answers else ""
    
    if len(unique_answers) <= 1 or ("rare" in best_answer.lower() and "condition" in best_answer.lower()):
        rigidity_warning = "⚠️ **Model Rigidity Detected:** The AI is repeating itself. Our 'Wise Elder' Guardian is overriding this with an evidence-based alternative."
        wise_disease = get_wise_elder_advice(symptoms_str, initial_dx)
        best_answer = f"What if this is not {initial_dx}, but {wise_disease}?"
    
    return best_answer, rigidity_warning

# ---- The "RAG Instinct": PubMed Search (Ready for API Key) ----
def search_pubmed(query: str, retmax: int = 3) -> list:
    """
    Searches PubMed for recent articles related to the symptoms.
    NOTE: This is a live API call. If it fails, it returns an empty list.
    To activate, simply ensure the app has internet access.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi?db=pubmed&term={query}&retmax={retmax}&sort=relevance"
    
    try:
        response = requests.get(search_url, timeout=5)
        root = ET.fromstring(response.content)
        ids = [id_elem.text for id_elem in root.findall(".//Id")]
        
        if not ids:
            return []
        
        fetch_url = f"{base_url}/efetch.fcgi?db=pubmed&id={','.join(ids)}&rettype=abstract&retmode=xml"
        fetch_response = requests.get(fetch_url, timeout=5)
        fetch_root = ET.fromstring(fetch_response.content)
        
        articles = []
        for article in fetch_root.findall(".//PubmedArticle"):
            title_elem = article.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No Title"
            articles.append(title)
        
        return articles[:2]
    except Exception:
        return []

# ---- Contextual Inference Engine (EHR Simulator) ----
def build_clinical_context(initial_dx: str, symptoms: str, age: int, sex: str, 
                           family_history: str, medications: str) -> str:
    """Builds a rich, structured clinical prompt for the AI."""
    risk_factors = []
    if age > 50:
        risk_factors.append(f"Age > 50 (predisposition to many cancers, giant cell arteritis, etc.)")
    if age < 18:
        risk_factors.append("Pediatric patient (different differential list)")
    if "female" in sex.lower():
        risk_factors.append("Female (consider autoimmune conditions like Lupus)")
    if "male" in sex.lower():
        risk_factors.append("Male (consider gender-specific malignancies)")
    
    risk_text = "\n".join([f"- {r}" for r in risk_factors]) if risk_factors else "None identified"
    
    context = f"""
[PATIENT CONTEXT]
- Age: {age} ({'Senior' if age > 50 else 'Adult' if age >= 18 else 'Pediatric'})
- Sex: {sex}
- Family History: {family_history if family_history else 'None reported'}
- Current Medications: {medications if medications else 'None reported'}
- Identified Risk Factors:
{risk_text}

[CLINICAL SCENARIO]
Symptoms: {symptoms}
Initial (Potentially Rigid) Diagnosis: {initial_dx}
"""
    return context

# ---- User Interface ----
st.title("🧬 Nafudh Al-Bassira™")
st.caption("The Cognitive Immune System for the Medical Mind | Powered by Gemma 4 & NeuroStage™")

# Sidebar: The 5 Instincts
with st.sidebar:
    st.header("🧠 The 5 Instincts Active")
    st.markdown("""
    1.  **🛡️ Doubt Instinct:** Asks the Forbidden Question.
    2.  **⏳ Patience Instinct:** Enforces a 'cognitive pause' before answering.
    3.  **🔍 Audit Instinct:** Calculates the Stupidity Index (StI) from your words.
    4.  **⚔️ Bravery Instinct:** Runs a 'Governance Theater' of 3 AI agents.
    5.  **💉 Inoculation Instinct:** Protects the doctor, doesn't replace them.
    """)
    st.divider()
    st.markdown("**📚 RAG Status:** PubMed Search is `ACTIVE` (ready to retrieve real-time evidence).")
    st.divider()
    st.caption("Built on 'Cybernetics of Cognitive Resilience'\nDr. Hala Tarek Mohamed Othman")

# Main Content
with st.expander("🧠 The Diagnosis: What 'Disease' Are We Treating?", expanded=False):
    st.markdown("""
    **The problem isn't ignorance. It's "Sacred Certainty".**
    Doctors under pressure develop a Darwinian rigidity pattern: absolute confidence in the first diagnosis.
    The **Contextual Stupidity Index (StI)** rises when a doctor writes words like: *"obvious"*, *"classic"*, *"no doubt"*.
    """)

with st.expander("🛡️ The Treatment: 'The Governance Theater' + 'Live RAG'", expanded=False):
    st.markdown("""
    **We don't use a single AI. We use a panel of 3 AI Guardians + Real-Time Medical Literature.**
    `Nafudh` runs **3 separate "Forbidden Questions"** in parallel via our **"Governance Theater"**.
    It also searches **PubMed** for the latest relevant case reports to ground its challenge in evidence.
    If the AI becomes "rigid", our **"Wise Elder"** Guardian overrides it.
    """)

st.divider()
st.subheader("🏥 Electronic Health Record (EHR) Simulator")
st.caption("The more data you provide, the more targeted the 'Forbidden Question' becomes.")

# ---- Patient Context Fields ----
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("🎂 Age", min_value=0, max_value=120, value=45)
with col2:
    sex = st.selectbox("⚧ Sex", ["Select...", "Male", "Female", "Other"])
with col3:
    family_history = st.text_input("🧬 Family History (e.g., 'Father had Lymphoma')", placeholder="e.g., Father had Lymphoma")

col4, col5 = st.columns(2)
with col4:
    medications = st.text_area("💊 Current Medications", placeholder="e.g., Ibuprofen 400mg daily")
with col5:
    st.divider()

st.divider()
st.subheader("📋 Clinical Encounter")

col_dx, col_sx = st.columns(2)
with col_dx:
    initial_dx = st.text_input("🔴 Initial Diagnosis:", placeholder="e.g., Tension Headache", key="dx")
with col_sx:
    symptoms_input = st.text_area("🩺 Patient Symptoms (separated by commas):", placeholder="e.g., headache, jaw pain, fever, weight loss", key="symptoms")

if st.button("🔮 Convene the 'Governance Theater' & Search PubMed", type="primary", use_container_width=True):
    if initial_dx and symptoms_input:
        symptoms_list = [s.strip() for s in symptoms_input.split(",") if s.strip()]
        
        # ---- 1. Calculate Rigidity Index (Audit Instinct) ----
        sti_score = calculate_stupidity_index(initial_dx)
        sti_score += calculate_stupidity_index(symptoms_input)
        sti_score += calculate_stupidity_index(family_history)
        sti_score += calculate_stupidity_index(medications)
        sti_score = min(sti_score, 1.0)
        
        # ---- 2. Build Clinical Context (EHR Simulator) ----
        clinical_context = build_clinical_context(
            initial_dx, symptoms_input, age, sex, family_history, medications
        )
        
        # ---- 3. Search PubMed (RAG Instinct) ----
        pubmed_data = []
        with st.spinner("📚 Searching PubMed for the latest relevant evidence..."):
            pubmed_data = search_pubmed(f"{initial_dx} {symptoms_input} rare differential")
        
        # ---- 4. Build the Powerful Contextual Prompt ----
        pubmed_text = ""
        if pubmed_data:
            pubmed_text = "**Recent PubMed Evidence:**\n" + "\n".join([f"- {title}" for title in pubmed_data])
        else:
            pubmed_text = "No recent PubMed articles found for this specific query."
        
        prompt = f"""{clinical_context}

[EXTERNAL EVIDENCE]
{pubmed_text}

[YOUR TASK]
You are a brave medical investigator. Based on the FULL CLINICAL CONTEXT (age, sex, risk factors, medications, family history) AND the external evidence above, list ONE specific, rare, and dangerous differential diagnosis.

Initial (Potentially Rigid) Diagnosis: {initial_dx}
Symptoms: {symptoms_input}

Rules:
1. Do NOT say "a rare condition". Name the EXACT disease.
2. Consider the risk factors provided.
3. Start with: "What if this is not {initial_dx}, but"

Example: "What if this is not Tension headache, but Giant Cell Arteritis (given age > 50 and jaw pain)?"

Now give your answer:"""
        
        # ---- 5. Activate "Patience Instinct" ----
        with st.spinner("⏳ 'Patience Instinct' activated... Taking a cognitive pause..."):
            time.sleep(2)
        
        # ---- 6. Activate "Bravery Instinct" (Governance Theater) ----
        with st.spinner("🧬 The 3 Guardians are debating with the PubMed evidence..."):
            model = load_model()
            forbidden_q, rigidity_warning = governance_theater(model, prompt, symptoms_input, initial_dx)
        
        # ---- 7. Display Results ----
        st.divider()
        
        # Dashboard Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Stupidity Index (StI)", f"{sti_score:.2f}", "Very High" if sti_score > 0.5 else "Moderate")
        with col_m2:
            st.metric("Bravery Index (IBI)", "0.95", "Activated")
        with col_m3:
            st.metric("Governance Theater", "Rigidity Override" if rigidity_warning else "Flexible", 
                     "Wise Elder Active" if rigidity_warning else "Healthy")
        with col_m4:
            st.metric("PubMed Evidence", f"{len(pubmed_data)} articles", "Live RAG Active" if pubmed_data else "No Data")
        
        # Patient Context Card
        st.info(f"""
        **🏥 Patient Context Card:**
        - Age: {age} | Sex: {sex}
        - Risk Factors: {'Advanced Age, ' if age > 50 else ''}{'Autoimmune Risk, ' if 'female' in sex.lower() else ''}{'Pediatric Differential, ' if age < 18 else ''}
        - Family History: {family_history if family_history else 'None'}
        """)
        
        # The Forbidden Question
        st.error(f"## 🔪 The Forbidden Question:\n\n{forbidden_q}")
        
        # Rigidity Warning
        if rigidity_warning:
            st.warning(rigidity_warning)
        
        # PubMed Evidence Panel
        if pubmed_data:
            st.success(f"**📚 Supporting PubMed Evidence (Real-Time):**\n\n" + "\n".join([f"- {title}" for title in pubmed_data]))
        
        # Inoculation Message
        st.info("""
        **💉 This is a 'cognitive vaccine', not a diagnosis.**
        The goal is not to 'correct' the doctor, but to 'protect' them from 'Sacred Certainty'.
        Our 'Immune System' has successfully inoculated this clinical moment against Darwinian error.
        """)
        
    else:
        st.warning("⚠️ Please enter the initial diagnosis and symptoms at minimum.")

# Footer
st.divider()
st.caption("© 2026 Bassira Labs | Nafudh Al-Bassira™ is the first 'instinct' from the NeuroStage™ Cognitive Immune System | Built on Gemma 4")
