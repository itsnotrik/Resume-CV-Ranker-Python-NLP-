import os
import docx
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def rank_resumes(job_desc_text, resumes_folder):
    results = []
    job_desc_processed = preprocess(job_desc_text)
    resume_texts = []

    filenames = os.listdir(resumes_folder)
    for filename in filenames:
        if filename.endswith(".docx"):
            text = extract_text_from_docx(os.path.join(resumes_folder, filename))
            processed = preprocess(text)
            resume_texts.append((filename, processed))

    texts = [job_desc_processed] + [text for _, text in resume_texts]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(texts)

    cosine_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    for (filename, _), score in zip(resume_texts, cosine_scores):
        results.append((filename, round(score * 100, 2)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results
