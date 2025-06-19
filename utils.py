from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import os
import uuid
import en_core_web_sm

nlp = en_core_web_sm.load()

def extract_resume_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_local_summary(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:3])  # Top 3 lines

def get_keywords_to_improve(resume, job_desc):
    resume_doc = nlp(resume.lower())
    job_doc = nlp(job_desc.lower())
    resume_words = set([token.text for token in resume_doc if token.is_alpha])
    job_words = set([token.text for token in job_doc if token.is_alpha])
    missing = list(job_words - resume_words)
    return ", ".join(sorted(missing[:10]))

def get_skills_to_improve(text):
    keywords = ["Python", "SQL", "Machine Learning", "Tableau", "Communication", "Teamwork"]
    missing = [skill for skill in keywords if skill.lower() not in text.lower()]
    return ", ".join(missing) if missing else "Resume covers most essential skills."

def get_similarity_score(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)

def export_ranking_pdf(ranking_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Resume Ranking Report", ln=True, align='C')
    pdf.ln(10)
    for name, score in ranking_list:
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{name} — Match Score: {score}%", ln=True)
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", f"{uuid.uuid4().hex}_ranking.pdf")
    pdf.output(file_path)
    return file_path

def get_openai_roles(resume_text):
    keywords = {
        "Python": "Python Developer",
        "SQL": "Data Analyst",
        "Machine Learning": "ML Engineer",
        "Tableau": "BI Analyst",
        "Deep Learning": "AI Researcher",
        "Cloud": "Cloud Engineer",
        "Spark": "Big Data Engineer",
        "NLP": "NLP Specialist"
    }
    matches = [role for kw, role in keywords.items() if kw.lower() in resume_text.lower()]
    return ", ".join(set(matches[:3])) or "Data Analyst, Software Developer, QA Engineer"
