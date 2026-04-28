from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding_score(resume, job_desc):
    emb1 = model.encode([resume])
    emb2 = model.encode([job_desc])
    score = cosine_similarity(emb1, emb2)
    return score[0][0] * 100
def combine_scores(embedding_score, llm_score):
    final_score = (embedding_score * 0.6) + (llm_score * 0.4)
    return round(final_score, 2)