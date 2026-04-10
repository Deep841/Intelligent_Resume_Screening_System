import streamlit as st
import os
import sys
import pandas as pd

# 🔥 Page config FIRST
st.set_page_config(page_title="Intelligent Resume Screening System", layout="wide")

# 🔥 Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.extraction.extractor import extract_text
from src.preprocessing.clean import clean_text
from src.features.skills import extract_skills
from src.jd_parser.parser import parse_job_description
from src.ranking.scorer import calculate_score, semantic_score

st.title("🚀 Intelligent Resume Screening System")

# Upload JD
jd_file = st.file_uploader("📄 Upload Job Description", type=["pdf", "docx"])

# Upload resumes
resume_files = st.file_uploader("📂 Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)

if st.button("🔍 Analyze Candidates"):

    if not jd_file or not resume_files:
        st.warning("Please upload both JD and resumes")
    
    else:
        # Save JD
        jd_path = "temp_jd.docx"
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())

        jd_text = extract_text(jd_path)
        jd_clean = clean_text(jd_text)

        jd_data = parse_job_description(jd_clean)
        jd_skills = jd_data["required_skills"]

        st.subheader("📌 JD Skills")
        st.write(jd_skills)

        results = []

        for resume in resume_files:
            temp_path = f"temp_{resume.name}"
            
            with open(temp_path, "wb") as f:
                f.write(resume.read())

            text = extract_text(temp_path)
            clean = clean_text(text)
            skills = extract_skills(clean)

            score, matched, reason = calculate_score(skills, jd_skills)

            semantic = semantic_score(clean, jd_clean)
            final_score = (0.7 * score) + (0.3 * semantic)

            missing = list(set(jd_skills) - set(matched))

            results.append({
                "Name": resume.name,
                "Score": round(final_score, 2),
                "Matched Skills": ", ".join(matched),
                "Missing Skills": missing,
                "Reason": reason
            })

        # 🔥 Sort correctly
        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        if results:   # 🔥 SAFE CHECK

            # 🔥 Top Candidate
            st.subheader("🏆 Top Candidate")
            st.success(f"{results[0]['Name']} → Score: {results[0]['Score']}%")

            # 🔥 DataFrame
            df = pd.DataFrame(results)

            # Display with %
            df_display = df.copy()
            df_display["Score"] = df_display["Score"].astype(str) + "%"

            st.subheader("📊 All Candidates")
            st.dataframe(df_display)

            # 🔥 Skill Gap
            st.subheader("⚠️ Skill Gap Analysis")
            for r in results:
                if r["Missing Skills"]:
                    st.error(f"{r['Name']} Missing Skills: {r['Missing Skills']}")

            # 🔥 Chart (numeric)
            st.subheader("📈 Score Comparison")
            chart_data = df.set_index("Name")["Score"]
            st.bar_chart(chart_data)

            # 🔥 Download
            st.download_button(
                label="📥 Download Results as CSV",
                data=df_display.to_csv(index=False),
                file_name="ranking_results.csv",
                mime="text/csv"
            )