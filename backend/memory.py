from backend.db import SessionLocal, Memory
from sentence_transformers import SentenceTransformer
import numpy as np

# 🔥 Load embedding model (runs once)
model = SentenceTransformer("all-MiniLM-L6-v2")


# 🔧 Convert text → embedding vector
def get_embedding(text: str):
    return model.encode(text).tolist()


# 💾 Save memory with embedding
def save_memory(prompt, response):
    db = SessionLocal()

    embedding = get_embedding(prompt)

    entry = Memory(
        prompt=prompt,
        response=response,
        embedding=embedding
    )

    db.add(entry)
    db.commit()
    db.close()

    print("✅ Memory saved:", prompt)


# 📏 Cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 🔍 Retrieve most relevant memories
def get_memory(query, limit=3):
    db = SessionLocal()

    memories = db.query(Memory).all()

    db.close()

    if not memories:
        return []

    query_emb = get_embedding(query)

    scored = []

    for m in memories:
        if m.embedding:
            try:
                score = cosine_similarity(query_emb, m.embedding)
                scored.append((score, m))
            except:
                continue

    # Sort by similarity
    scored.sort(reverse=True, key=lambda x: x[0])

    top_memories = scored[:limit]

    return [
        f"Prompt: {m.prompt}\nResponse: {m.response}"
        for _, m in top_memories
    ]