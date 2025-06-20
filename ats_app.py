import streamlit as st
from utils import (
    extract_resume_text,
    get_local_summary,
    get_keywords_to_improve,
    get_skills_to_improve,
    get_similarity_score,
    export_ranking_pdf,
    get_openai_roles
)
import os

st.set_page_config(page_title="SmartHire ATS | Resume Analyzer", layout="wide")

st.markdown("## 🧠 **SmartHire ATS – Resume Analyzer**")
st.markdown("_A professional resume analysis tool for recruiters and job seekers._")
st.write("---")

# 📌 Analyze a Single Resume
st.header("📌 Analyze a Single Resume")

col1, col2 = st.columns([1, 1])
with col1:
    resume_file = st.file_uploader("Upload your Resume", type=["pdf"])
with col2:
    job_description_text = st.text_area("Paste Job Description Below", height=200)

if resume_file and job_description_text:
    resume_text = extract_resume_text(resume_file)

    st.subheader("📋 Summary of Resume")
    st.success(get_local_summary(resume_text))

    st.subheader("🔍 Keywords to Improve")
    st.info(get_keywords_to_improve(resume_text, job_description_text))

    st.subheader("🎯 Skills to Improve")
    st.warning(get_skills_to_improve(resume_text))

    st.subheader("📊 Match Score")
    score = get_similarity_score(resume_text, job_description_text)
    st.progress(int(score))
    st.success(f"Resume Match Score: **{score}%**")

st.write("---")

# 📊 Rank Multiple Resumes
st.header("📊 Rank Multiple Resumes for One Job")

jd_file = st.text_area("Paste Job Description for Ranking", height=150)
resume_files = st.file_uploader("Upload Multiple Resumes", type=["pdf"], accept_multiple_files=True)

if jd_file and resume_files:
    rankings = []
    for res in resume_files:
        res_text = extract_resume_text(res)
        sim = get_similarity_score(res_text, jd_file)
        rankings.append((res.name, sim))

    rankings = sorted(rankings, key=lambda x: x[1], reverse=True)

    st.subheader("🏆 Ranking Results")
    for name, score in rankings:
        st.success(f"{name} — Match Score: {score}%")

    if st.button("📥 Download Ranking as PDF"):
        path = export_ranking_pdf(rankings)
        with open(path, "rb") as f:
            st.download_button(label="Download", data=f, file_name="ranking_report.pdf")

st.write("---")

# 💼 Suggest Suitable Job Roles
st.header("💼 Suggest Suitable Job Roles")

role_file = st.file_uploader("Upload Resume for Role Suggestions", type=["pdf"])
if role_file:
    role_text = extract_resume_text(role_file)
    roles = get_openai_roles(role_text)
    st.success("Suggested Job Roles:")
    st.markdown(f"- {roles.replace(', ', '\n- ')}")
