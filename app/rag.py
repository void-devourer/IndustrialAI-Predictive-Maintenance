import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

def retrieve_knowledge(query: str, limit: int = 3):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, content, source
        FROM knowledge_documents
        ORDER BY id DESC
    """)

    documents = cur.fetchall()

    query_words = {
        word.lower().strip(".,!?")
        for word in query.split()
        if len(word) > 3
    }

    results = []

    for doc_id, title, content, source in documents:
        text = content.lower()

        score = sum(
            1
            for word in query_words
            if word in text
        )

        results.append({
            "id": doc_id,
            "title": title,
            "content": content,
            "source": source,
            "score": score,
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    cur.close()
    conn.close()

    return results[:limit]