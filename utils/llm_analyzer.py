from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def analyze_resume(resume, job_desc):
    prompt = f"""
You are an AI recruiter.

Return ONLY JSON. No explanation.

{{
 "match_score": number between 0 and 100,
 "matched_skills": [],
 "missing_skills": [],
 "suggestions": []
}}

Resume:
{resume}

Job Description:
{job_desc}
"""
    response = llm.invoke(prompt)
    return response