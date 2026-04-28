from flask import Flask, render_template, request
from utils.parser import extract_text_from_pdf
from utils.preprocess import clean_text
from utils.matcher import get_embedding_score, combine_scores
from utils.llm_analyzer import analyze_resume
import re 
import json

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    final_score = None
    llm_data = {
        "match_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "suggestions": []
    }

    if request.method == "POST":

     file = request.files.get("resume")
     job_desc = request.form.get("job_desc")

     if file and job_desc:
        resume_text = extract_text_from_pdf(file)
        resume_clean = clean_text(resume_text)
        job_clean = clean_text(job_desc)

        embedding_score = get_embedding_score(resume_clean, job_clean)

        llm_result = analyze_resume(resume_clean, job_clean)

        import json

        try:
            llm_data = json.loads(llm_result)
        except:
            llm_data = {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "suggestions": []
            }

        llm_score = llm_data.get("match_score", 0)

        if llm_score <= 1:
            llm_score *= 100

        final_score = combine_scores(embedding_score, llm_score)
    return render_template(
    "index.html",
    score=final_score,
    result=llm_data
)
    
if __name__ == "__main__":
    app.run(debug=True)

    