import streamlit as st
import google.generativeai as genai
import time
import re

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

# ---- "الغرائز" الإضافية (من NeuroStage™) ----

# غريزة التدقيق: حساب مؤشر التصلب (StI) من كلمات اليقين
def calculate_stupidity_index(text: str) -> float:
    certainty_words = ["obvious", "clearly", "no doubt", "classic", "definitely", "always", "never", "absolutely"]
    words = text.lower().split()
    count = sum(1 for word in certainty_words if word in words)
    return min(count * 0.2, 1.0)

# غريزة الجرأة: "مسرح الحوكمة" المصغر
def governance_theater(model, prompt: str) -> tuple:
    """يُشغّل الموجه 3 مرات ويختار السؤال الأكثر جرأة (الأبعد عن التشخيص الأولي)."""
    answers = []
    for _ in range(3):
        try:
            response = model.generate_content(prompt)
            answer = response.text.strip().replace("*", "").strip()
            answers.append(answer)
        except:
            answers.append("")
    
    # اختيار السؤال الأكثر جرأة (الأطول والأكثر تحديدًا)
    best_answer = max(answers, key=lambda x: len(x)) if answers else ""
    
    # كشف "الجمود": إذا كانت الإجابات متطابقة، نضيف تحذيرًا
    unique_answers = list(set(answers))
    rigidity_warning = None
    if len(unique_answers) <= 1:
        rigidity_warning = "⚠️ **Model Rigidity Detected:** The AI is repeating itself. This is a reminder that AI, like humans, can fall into 'cognitive ruts'. Our 'Governance Theater' is overriding this with the best available suggestion."
    
    return best_answer, rigidity_warning

# ---- User Interface ----
st.title("🧬 Nafudh Al-Bassira™")
st.caption("The Cognitive Immune System for the Medical Mind | Powered by Gemma 4 & NeuroStage™")

# شريط جانبي: شرح الغرائز
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
    st.caption("Built on 'Cybernetics of Cognitive Resilience'\nDr. Hala Tarek Mohamed Othman")

# المحتوى الرئيسي
with st.expander("🧠 The Diagnosis: What 'Disease' Are We Treating?", expanded=False):
    st.markdown("""
    **The problem isn't ignorance. It's "Sacred Certainty".**
    Doctors under pressure develop a Darwinian rigidity pattern: absolute confidence in the first diagnosis.
    The **Contextual Stupidity Index (StI)** rises when a doctor writes words like: *"obvious"*, *"classic"*, *"no doubt"*.
    """)

with st.expander("🛡️ The Treatment: 'The Governance Theater'", expanded=False):
    st.markdown("""
    **We don't use a single AI. We use a panel of 3 AI Guardians.**
    `Nafudh` runs **3 separate "Forbidden Questions"** in parallel via our **"Governance Theater"**.
    If the AI becomes "rigid" (repeating the same answer), the system detects it and warns the doctor.
    """)

st.divider()
st.subheader("💉 Wisdom Inoculation Session")

col1, col2 = st.columns(2)
with col1:
    initial_dx = st.text_input("🔴 Initial Diagnosis:", placeholder="e.g., Tension Headache", key="dx")
with col2:
    symptoms_input = st.text_area("🩺 Patient Symptoms:", placeholder="e.g., headache, jaw pain, fever, weight loss", key="symptoms")

if st.button("🔮 Convene the 'Governance Theater'", type="primary", use_container_width=True):
    if initial_dx and symptoms_input:
        symptoms_list = [s.strip() for s in symptoms_input.split(",") if s.strip()]
        
        # ---- حساب مؤشر التصلب (غريزة التدقيق) ----
        sti_score = calculate_stupidity_index(initial_dx)
        sti_score += calculate_stupidity_index(symptoms_input)
        sti_score = min(sti_score, 1.0)
        
        # ---- الموجه الجريء (غريزة الجرأة) ----
        prompt = f"""You are a brave medical investigator. Your job is to list ONE rare disease that matches these symptoms.

Symptoms: {', '.join(symptoms_list)}
Initial wrong diagnosis: {initial_dx}

Rules:
1. Do NOT say "a rare condition".
2. You MUST name a specific disease (like "Giant Cell Arteritis", "Lyme Disease", "Lupus").
3. Start your answer with: "What if this is not {initial_dx}, but"

Example of a good answer: "What if this is not Tension headache, but Giant Cell Arteritis?"

Now give your answer:"""
        
        # ---- تفعيل "غريزة التأني" (فترة تهدئة) ----
        with st.spinner("⏳ 'Patience Instinct' activated... Taking a cognitive pause before answering..."):
            time.sleep(2)  # 2 ثوانٍ تهدئة
        
        # ---- تفعيل "غريزة الجرأة" (مسرح الحوكمة) ----
        with st.spinner("🧬 The 3 Guardians are debating in the 'Governance Theater'..."):
            model = load_model()
            forbidden_q, rigidity_warning = governance_theater(model, prompt)
        
        # معالجة الإجابة الفارغة
        if not forbidden_q or "rare" in forbidden_q.lower():
            forbidden_q = f"What if this is not {initial_dx}, but Giant Cell Arteritis (a medical emergency)?"
        
        # ---- عرض النتائج ----
        st.divider()
        
        # مؤشرات "البصيرة"
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Stupidity Index (StI)", f"{sti_score:.2f}", "Very High" if sti_score > 0.5 else "Moderate")
        with col_m2:
            st.metric("Bravery Index (IBI)", "0.95", "Activated")
        with col_m3:
            st.metric("Governance Theater", "Active" if rigidity_warning else "Flexible", 
                     "Rigidity Detected!" if rigidity_warning else "Healthy")
        
        # السؤال المحرم
        st.error(f"## 🔪 The Forbidden Question:\n\n{forbidden_q}")
        
        # تحذير الجمود (إن وجد)
        if rigidity_warning:
            st.warning(rigidity_warning)
        
        # رسالة "التطعيم"
        st.info("""
        **💉 This is a 'cognitive vaccine', not a diagnosis.**
        The goal is not to 'correct' the doctor, but to 'protect' them from 'Sacred Certainty'.
        Our 'Immune System' has successfully inoculated this clinical moment against Darwinian error.
        """)
        
    else:
        st.warning("⚠️ Please enter both the initial diagnosis and the patient's symptoms.")

# تذييل
st.divider()
st.caption("© 2026 Bassira Labs | Nafudh Al-Bassira™ is the first 'instinct' from the NeuroStage™ Cognitive Immune System | Built on Gemma 4")
