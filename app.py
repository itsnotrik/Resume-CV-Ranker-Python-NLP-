import streamlit as st
from utils import rank_resumes
import os

st.title("🧠 Resume/CV Ranker")
st.write("Upload a job description and a folder of resumes to see which candidates match best.")

job_description = st.text_area("Paste Job Description Here:")

uploaded_resumes = st.file_uploader("Upload Resume Files (.docx)", accept_multiple_files=True, type=["docx"])

if st.button("Rank Resumes"):
    if not job_description or not uploaded_resumes:
        st.warning("Please upload a job description and at least one resume.")
    else:
        folder = "resumes"
        os.makedirs(folder, exist_ok=True)
        for resume in uploaded_resumes:
            with open(os.path.join(folder, resume.name), "wb") as f:
                f.write(resume.getbuffer())

        results = rank_resumes(job_description, folder)

        st.subheader("Ranking Results")
        for i, (filename, score) in enumerate(results, start=1):
            st.write(f"{i}. **{filename}** - Match Score: `{score}%`")
