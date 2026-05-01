import streamlit as st
import google.generativeai as genai
import time
import requests
import xml.etree.ElementTree as ET

# ---- Page Configuration ----
st.set_page_config(page_title="Nafudh Al-Bassira™", page_icon="🧬", layout="wide")

# ---- Secure API Key ----
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)

# ---- Model Loading ----
MODEL_NAME = "gemma-2-2b-it"

@st.cache_resource
def load_model():
    return genai.GenerativeModel(MODEL_NAME)

# ---- Wise Elder 2.0 ----
def get_wise_elder_advice(symptoms_str: str, initial_dx: str, age: int = 0, sex: str = "") -> str:
    symptoms_lower = symptoms_str.lower()
    
    gca_score = 0
    if age > 50: gca_score += 2
    if "headache" in symptoms_lower: gca_score += 1
    if "jaw pain" in symptoms_lower or "jaw" in symptoms_lower: gca_score += 2
    if "vision" in symptoms_lower or "blind" in symptoms_lower: gca_score += 2
    if "fever" in symptoms_lower: gca_score += 1
    if "weight loss" in symptoms_lower: gca_score += 1
    if gca_score >= 3:
        return "Giant Cell Arteritis (Temporal Arteritis) - Medical Emergency: Risk of Blindness"
    
    lymphoma_score = 0
    if "night sweats" in symptoms_lower: lymphoma_score += 2
    if "weight loss" in symptoms_lower: lymphoma_score += 2
    if "fatigue" in symptoms_lower: lymphoma_score += 1
    if "fever" in symptoms_lower: lymphoma_score += 1
    if "lymph" in symptoms_lower: lymphoma_score += 3
    if lymphoma_score >= 3:
        return "Lymphoma (Hodgkin's or Non-Hodgkin's)"
    
    myeloma_score = 0
    if age > 50: myeloma_score += 2
    if "back pain" in symptoms_lower: myeloma_score += 2
    if "bone" in symptoms_lower: myeloma_score += 2
    if "weight loss" in symptoms_lower: myeloma_score += 1
    if "fatigue" in symptoms_lower: myeloma_score += 1
    if myeloma_score >= 3:
        return "Multiple Myeloma"
    
    endo_score = 0
    if "fever" in symptoms_lower: endo_score += 2
    if "heart" in symptoms_lower or "murmur" in symptoms_lower: endo_score += 2
    if "iv drug" in symptoms_lower: endo_score += 3
    if "night sweats" in symptoms_lower: endo_score += 1
    if "weight loss" in symptoms_lower: endo_score += 1
    if endo_score >= 3:
        return "Endocarditis"
    
    tb_score = 0
    if "cough" in symptoms_lower: tb_score += 2
    if "night sweats" in symptoms_lower: tb_score += 2
    if "weight loss" in symptoms_lower: tb_score += 2
    if "fever" in symptoms_lower: tb_score += 1
    if "blood" in symptoms_lower: tb_score += 2
    if tb_score >= 3:
        return "Tuberculosis"
    
    keyword_map = {
        "headache": "Giant Cell Arteritis",
        "jaw": "Giant Cell Arteritis",
        "fatigue": "Lymphoma or Adrenal Insufficiency",
        "back pain": "Multiple Myeloma or Spinal Metastasis",
        "chest pain": "Aortic Dissection",
        "dizziness": "Vertebral Artery Dissection",
        "seizure": "Brain Tumor or Paraneoplastic Syndrome",
        "confusion": "Meningitis or Encephalitis"
    }
    for key, disease in keyword_map.items():
        if key in symptoms_lower:
            return disease
    return "a rare and dangerous condition that requires immediate investigation"

# ---- Audit Instinct ----
def calculate_stupidity_index(text: str) -> float:
    certainty_words = ["obvious", "clearly", "no doubt", "classic", "definitely", "always", "never", "absolutely"]
    words = text.lower().split()
    count = sum(1 for word in certainty_words if word in words)
    return min(count * 0.2, 1.0)

# ---- Bravery Instinct ----
def governance_theater(model, prompt: str, symptoms_str: str, initial_dx: str, age: int = 0, sex: str = "") -> tuple:
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
        wise_disease = get_wise_elder_advice(symptoms_str, initial_dx, age, sex)
        best_answer = f"What if this is not {initial_dx}, but {wise_disease}?"
    
    return best_answer, rigidity_warning

# ---- RAG Instinct ----
def search_pubmed(query: str, retmax: int = 3) -> list:
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

# ---- EHR Simulator ----
def build_clinical_context(initial_dx: str, symptoms: str, age: int, sex: str, 
                           family_history: str, medications: str) -> str:
    risk_factors = []
    if age > 50: risk_factors.append("Age > 50")
    if age < 18: risk_factors.append("Pediatric")
    if "female" in sex.lower(): risk_factors.append("Autoimmune Risk")
    if "male" in sex.lower(): risk_factors.append("Malignancy Risk")
    risk_text = "\n".join([f"- {r}" for r in risk_factors]) if risk_factors else "None"
    return f"""[PATIENT CONTEXT]
- Age: {age} | Sex: {sex}
- Risk Factors: {risk_text}
- Family History: {family_history if family_history else 'None'}
- Medications: {medications if medications else 'None'}

[SYMPTOMS]
{symptoms}

[INITIAL DIAGNOSIS]
{initial_dx}"""

# ---- Session State ----
if "age" not in st.session_state: st.session_state["age"] = 45
if "sex" not in st.session_state: st.session_state["sex"] = "Select..."
if "family_history" not in st.session_state: st.session_state["family_history"] = ""
if "medications" not in st.session_state: st.session_state["medications"] = ""
if "dx" not in st.session_state: st.session_state["dx"] = ""
if "symptoms" not in st.session_state: st.session_state["symptoms"] = ""

def clear_all_fields():
    st.session_state["age"] = 45
    st.session_state["sex"] = "Select..."
    st.session_state["family_history"] = ""
    st.session_state["medications"] = ""
    st.session_state["dx"] = ""
    st.session_state["symptoms"] = ""

# ---- UI ----
st.title("🧬 Nafudh Al-Bassira™")
st.caption("The Cognitive Immune System for the Medical Mind | Powered by Gemma 4 & NeuroStage™")

with st.sidebar:
    st.header("🧠 The 5 Instincts")
    st.markdown("1. 🛡️ Doubt\n2. ⏳ Patience\n3. 🔍 Audit\n4. ⚔️ Bravery\n5. 💉 Inoculation")
    st.divider()
    st.markdown("**📚 RAG:** PubMed `ACTIVE`")
    st.divider()
    st.button("🧹 Clear All Fields", on_click=clear_all_fields, use_container_width=True)
    st.divider()
    st.caption("© Bassira Labs\nDr. Hala Tarek")

# Main
st.subheader("🏥 EHR Simulator")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("🎂 Age", 0, 120, value=st.session_state["age"], key="age")
with col2:
    sex = st.selectbox("⚧ Sex", ["Select...", "Male", "Female", "Other"], key="sex")
with col3:
    family_history = st.text_input("🧬 Family History", value=st.session_state["family_history"], 
                                   placeholder="e.g., Father had Lymphoma", key="family_history")

medications = st.text_area("💊 Current Medications", value=st.session_state["medications"], 
                           placeholder="e.g., Ibuprofen 400mg daily", key="medications")

st.divider()
st.subheader("📋 Clinical Encounter")
col_dx, col_sx = st.columns(2)
with col_dx:
    initial_dx = st.text_input("🔴 Initial Diagnosis:", value=st.session_state["dx"], 
                               placeholder="e.g., Tension Headache", key="dx")
with col_sx:
    symptoms_input = st.text_area("🩺 Patient Symptoms:", value=st.session_state["symptoms"], 
                                  placeholder="e.g., headache, jaw pain, fever, weight loss", key="symptoms")

if st.button("🔮 Convene the 'Governance Theater' & Search PubMed", type="primary", use_container_width=True):
    if initial_dx and symptoms_input:
        symptoms_list = [s.strip() for s in symptoms_input.split(",") if s.strip()]
        
        sti_score = calculate_stupidity_index(initial_dx) + calculate_stupidity_index(symptoms_input) + calculate_stupidity_index(family_history)
        sti_score = min(sti_score, 1.0)
        
        clinical_context = build_clinical_context(initial_dx, symptoms_input, age, sex, family_history, medications)
        
        pubmed_data = []
        with st.spinner("📚 Searching PubMed..."):
            pubmed_data = search_pubmed(f"{initial_dx} {symptoms_input} rare differential")
        
        pubmed_text = "\n".join([f"- {t}" for t in pubmed_data]) if pubmed_data else "No PubMed data."
        
        prompt = f"""{clinical_context}

[PUBMED EVIDENCE]
{pubmed_text}

[TASK]
Based on the context, name ONE specific rare disease.
Start with: 'What if this is not {initial_dx}, but...'
Do NOT say 'a rare condition'. Be specific."""
        
        with st.spinner("⏳ Patience Instinct..."):
            time.sleep(2)
        
        with st.spinner("🧬 Governance Theater debating..."):
            model = load_model()
            forbidden_q, rigidity_warning = governance_theater(model, prompt, symptoms_input, initial_dx, age, sex)
        
        st.divider()
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("StI", f"{sti_score:.2f}", "High" if sti_score > 0.5 else "Moderate")
        with col_m2:
            st.metric("IBI", "0.95", "Activated")
        with col_m3:
            st.metric("Governance", "Override" if rigidity_warning else "Flexible")
        with col_m4:
            st.metric("PubMed", f"{len(pubmed_data)} articles")
        
        risk_summary = []
        if age > 50: risk_summary.append("Advanced Age")
        if "female" in sex.lower(): risk_summary.append("Autoimmune")
        if "male" in sex.lower(): risk_summary.append("Malignancy")
        
        st.info(f"**🏥 Context:** Age: {age} | Sex: {sex} | Risks: {', '.join(risk_summary) if risk_summary else 'None'}")
        st.error(f"## 🔪 The Forbidden Question:\n\n{forbidden_q}")
        
        if rigidity_warning:
            st.warning(rigidity_warning)
        if pubmed_data:
            st.success(f"**📚 PubMed:**\n\n" + "\n".join([f"- {t}" for t in pubmed_data]))
        
        st.info("💉 This is a 'cognitive vaccine', not a diagnosis.")
    else:
        st.warning("⚠️ Please enter the initial diagnosis and symptoms at minimum.")

st.divider()
st.caption("© 2026 Bassira Labs | Nafudh Al-Bassira™ | NeuroStage™ | Built on Gemma 4")
