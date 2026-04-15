import streamlit as st
import os
import sys
import pandas as pd
import tempfile
from pathlib import Path
import re

# ---------- Page Config ----------
st.set_page_config(
    page_title="Intelligent Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# ---------- Path Fix ----------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---------- Imports ----------
from src.extraction.extractor import extract_text
from src.preprocessing.clean import clean_text
from src.features.skills import extract_skills
from src.jd_parser.parser import parse_job_description
from src.ranking.scorer import calculate_score, semantic_score
from src.features.education import extract_education
from src.features.certifications import extract_certifications
from src.features.experience import extract_experience
from src.utils.github_ai import github_ai_feedback


# ---------- AI Score Extractor ----------
def extract_ai_score(ai_text):
    try:
        match = re.search(r"Score:\s*(\d+)", ai_text)
        if match:
            return int(match.group(1))
    except:
        pass
    return 0


# ---------- Utility ----------
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def process_job_description(jd_file):
    jd_path = save_uploaded_file(jd_file)
    jd_text = extract_text(jd_path)
    jd_clean = clean_text(jd_text)

    jd_data = parse_job_description(jd_clean)
    jd_skills = jd_data.get("required_skills", [])

    return jd_clean, jd_skills


def process_resume(resume_file, jd_clean, jd_skills):
    resume_path = save_uploaded_file(resume_file)

    text = extract_text(resume_path)
    cleaned_text = clean_text(text)

    skills = extract_skills(cleaned_text)
    education = extract_education(cleaned_text)
    certs = extract_certifications(cleaned_text)
    exp = extract_experience(cleaned_text)

    score, matched, reason = calculate_score(skills, jd_skills)
    semantic = semantic_score(cleaned_text, jd_clean)

    education_score = 10 if education else 0
    cert_score = 10 if certs else 0

    base_score = round(
        (0.6 * score) + (0.2 * semantic) + (0.1 * education_score) + (0.1 * cert_score),
        2
    )

    missing = sorted(list(set(jd_skills) - set(matched)))

    return {
        "Name": resume_file.name,
        "Score": base_score,
        "clean_text": cleaned_text,
        "Experience (Years)": exp,
        "Education": ", ".join(education) if education else "None",
        "Certifications": ", ".join(certs) if certs else "None",
        "Matched Skills": ", ".join(matched) if matched else "None",
        "Missing Skills": ", ".join(missing) if missing else "None",
        "Reason": reason,
        "AI Feedback": "",
        "AI Score": 0
    }


def analyze_candidates(jd_file, resume_files):
    jd_clean, jd_skills = process_job_description(jd_file)

    results = [
        process_resume(resume, jd_clean, jd_skills)
        for resume in resume_files
    ]

    # 🔥 SORT FIRST
    results = sorted(results, key=lambda x: x["Score"], reverse=True)

    # 🔥 Progress bar
    progress = st.progress(0)
    total = min(len(results), 2)

    # 🔥 AI ONLY FOR TOP 2
    for i, r in enumerate(results):
        if i < 2:

            status = st.empty()
            status.info(f"🤖 Running AI for {r['Name']}...")

            ai_feedback = github_ai_feedback(r["clean_text"], jd_clean)
            r["AI Feedback"] = ai_feedback

            # 🔥 Extract AI score
            ai_score = extract_ai_score(ai_feedback)
            r["AI Score"] = ai_score

            # 🔥 Boost score
            r["Score"] = round((0.75 * r["Score"]) + (0.25 * ai_score), 2)

            status.success(f"✅ AI analysis completed for {r['Name']}")
            progress.progress((i + 1) / total)

        else:
            r["AI Feedback"] = "Skipped to save API usage"

    progress.empty()
    st.success("🎉 All AI evaluations completed!")

    return jd_skills, results


# ---------- UI ----------
st.title("🚀 Intelligent Resume Screening System")
st.markdown("### AI-Powered Resume Ranking with Explainability")

col1, col2 = st.columns(2)

with col1:
    jd_file = st.file_uploader("📄 Upload Job Description", type=["pdf", "docx"])

with col2:
    resume_files = st.file_uploader(
        "📂 Upload Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

if st.button("🔍 Analyze Candidates", use_container_width=True):

    if not jd_file or not resume_files:
        st.warning("Please upload both JD and resumes.")
    else:
        with st.spinner("🔄 Processing resumes and running AI..."):
            try:
                jd_skills, results = analyze_candidates(jd_file, resume_files)

                st.success("✅ Analysis Completed Successfully")

                st.subheader("📌 Required JD Skills")
                st.write(jd_skills if jd_skills else "No skills detected")

                top_candidate = results[0]

                st.subheader("🏆 Top Candidate")
                st.success("🏆 AI Selected Candidate")

                c1, c2 = st.columns([2, 1])
                with c1:
                    st.success(f"**{top_candidate['Name']}** is the best match")
                with c2:
                    st.metric("Score", f"{top_candidate['Score']}%")

                df = pd.DataFrame(results).drop(columns=["clean_text"])

                st.subheader("📊 Candidate Ranking")
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.subheader("📈 Score Comparison")
                st.bar_chart(df.set_index("Name")["Score"])

                st.subheader("⚠️ Skill Gap Analysis")

                for row in results:
                    if row["Missing Skills"] != "None":
                        with st.expander(row["Name"]):
                            st.write(f"**Missing Skills:** {row['Missing Skills']}")
                            st.write(f"**Reason:** {row['Reason']}")

                st.subheader("🤖 AI Evaluation")

                for row in results:
                    with st.expander(f"{row['Name']}"):

                        ai_score = row.get("AI Score", 0)

                        if ai_score >= 80:
                            st.success("🔥 Highly Recommended by AI")
                        elif ai_score >= 60:
                            st.info("👍 Good Fit")
                        else:
                            st.warning("⚠️ Needs Improvement")

                        st.write(row["AI Feedback"])

                st.download_button(
                    label="📥 Download Results as CSV",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="ranking_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")