from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import requests

app = FastAPI(title="AskAI 2025")

DB_FILE = "qa.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS qa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_ai(q: Question):
    query = q.query
    answer = None

    # Choose AI backend: Ollama (local) or OpenAI API
    if os.getenv("USE_OLLAMA", "true") == "true":
        try:
            r = requests.post("http://host.docker.internal:11434/api/generate",
                              json={"model": "llama3", "prompt": query})
            data = r.json()
            answer = data.get("response", "No answer")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": query}]
        )
        answer = resp.choices[0].message.content

    # Save to DB
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO qa (question, answer) VALUES (?, ?)", (query, answer))
    conn.commit()
    conn.close()

    return {"question": query, "answer": answer}
