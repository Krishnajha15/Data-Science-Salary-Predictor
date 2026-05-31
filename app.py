import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Load model and encoders
model = joblib.load("salary_prediction_model.pkl")
encoders = joblib.load("model_columns.pkl")

st.set_page_config(page_title="DS Salary Predictor", page_icon="💰", layout="centered")

st.title("💰 Data Science Salary Predictor")
st.markdown("Apni job details bharo aur dekho kitni salary milni chahiye!")
st.divider()

col1, col2 = st.columns(2)

with col1:
    experience_level = st.selectbox("Experience Level", ["EN", "MI", "SE", "EX"],
        format_func=lambda x: {"EN":"🎓 Entry Level (0–2 yrs)","MI":"💼 Mid Level (2–5 yrs)",
                                "SE":"🏆 Senior Level (5+ yrs)","EX":"👔 Executive"}[x])
    years_experience = st.slider("Years of Experience", 0, 20, 2)
    employment_type = st.selectbox("Employment Type", ["FT", "PT", "CT", "FL"],
        format_func=lambda x: {"FT":"✅ Full Time","PT":"⏰ Part Time",
                                "CT":"📋 Contract","FL":"🧑‍💻 Freelance"}[x])
    remote_ratio = st.selectbox("Work Mode", [0, 50, 100],
        format_func=lambda x: {0:"🏢 Office (WFO)", 50:"🔀 Hybrid", 100:"🏠 Fully Remote"}[x])

with col2:
    company_size = st.selectbox("Company Size", ["S", "M", "L"],
        format_func=lambda x: {"S":"🏠 Small (<50)","M":"🏢 Medium (50–250)","L":"🏙️ Large (250+)"}[x])
    job_title = st.selectbox("Job Title", sorted(encoders['job_title'].classes_.tolist()))
    employee_residence = st.selectbox("Employee Country", sorted(encoders['employee_residence'].classes_.tolist()))
    company_location = st.selectbox("Company Country", sorted(encoders['company_location'].classes_.tolist()))

st.divider()

if st.button("🔮 Salary Predict Karo", use_container_width=True):

    def safe_encode(encoder, value):
        if value in encoder.classes_:
            return encoder.transform([value])[0]
        return 0

    input_data = pd.DataFrame([{
        "job_title":          safe_encode(encoders['job_title'], job_title),
        "experience_level":   safe_encode(encoders['experience_level'], experience_level),
        "employment_type":    safe_encode(encoders['employment_type'], employment_type),
        "company_location":   safe_encode(encoders['company_location'], company_location),
        "company_size":       safe_encode(encoders['company_size'], company_size),
        "employee_residence": safe_encode(encoders['employee_residence'], employee_residence),
        "remote_ratio":       remote_ratio,
        "years_experience":   years_experience,
    }])

    prediction = model.predict(input_data)[0]
    india_prediction = prediction * 0.18

    st.divider()
    col_us, col_in = st.columns(2)

    with col_us:
        st.metric(label="🌍 Global (US Market)", value=f"${prediction:,.0f}", delta="per year")
        st.caption(f"Monthly: ~${prediction/12:,.0f} USD")

    with col_in:
        st.metric(label="🇮🇳 India Equivalent", value=f"₹{india_prediction*83:,.0f}", delta="per year (approx)")
        st.caption(f"Monthly: ~₹{(india_prediction*83)/12:,.0f}")

    st.divider()
    annual_inr = india_prediction * 83
    if annual_inr >= 3000000:
        st.markdown("### 🚀 Top-tier role in India! Premium compensation.")
    elif annual_inr >= 1200000:
        st.markdown("### 💪 Solid market salary for India!")
    else:
        st.markdown("### 📈 Entry-level range — scope for growth!")

st.divider()
st.caption("Built with Python, XGBoost & Streamlit | Dataset: Kaggle AI Job Market 2025")