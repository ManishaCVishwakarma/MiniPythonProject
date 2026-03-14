import requests
import numpy as np
import pandas as pd

# -------- LM Studio API --------
EMBED_URL = "http://192.168.31.39:1234/v1/embeddings"
CHAT_URL = "http://192.168.31.39:1234/v1/chat/completions"

EMBED_MODEL = "text-embedding-all-minilm-l6-v2-embedding"
LLM_MODEL = "google/gemma-3-1b"

# -------- Load Excel --------
excel_path = "data/Stu_Data.xlsx"

df = pd.read_excel(excel_path)

# remove hidden spaces in column names
df.columns = df.columns.str.strip()

# convert decimal percentage to marks
df["Marks"] = (df["Marks"] * 100).astype(int)

# -------- Convert rows to text --------
chunks = []

for _, row in df.iterrows():
    text = f"Student ID {row['Student ID']} Name {row['Full Name']} Course {row['Course']} Marks {row['Marks']} Age {row['Age']}"
    chunks.append(text)

print("Total rows:", len(chunks))

# -------- Create Embeddings --------
chunk_embeddings = []

print("Creating embeddings...")

for chunk in chunks:

    response = requests.post(
        EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "input": chunk
        }
    )

    embedding = response.json()["data"][0]["embedding"]
    chunk_embeddings.append(embedding)

print("Embeddings ready!")

# -------- Cosine Similarity --------
def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -------- Question Function --------
def ask_question(question):

    # embedding for question
    response = requests.post(
        EMBED_URL,
        json={
            "model": EMBED_MODEL,
            "input": question
        }
    )

    q_embedding = response.json()["data"][0]["embedding"]

    scores = []

    for emb in chunk_embeddings:
        score = cosine_similarity(q_embedding, emb)
        scores.append(score)

    # -------- Top 5 rows retrieval --------
    top_k = 5
    top_indices = np.argsort(scores)[-top_k:]

    context = "\n".join([chunks[i] for i in top_indices])

    prompt = f"""
You are analyzing student data.

Use the context below to answer the question.

Context:
{context}

Question:
{question}

Give a clear answer.
"""

    response = requests.post(
        CHAT_URL,
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]

    print("\nQuestion:", question)
    print("\nAnswer:\n", answer)
    print("\n----------------------------\n")


# -------- First Question --------
ask_question("Who scored highest marks?")

print("Ask questions about the student dataset.")
print("Type 'exit' to stop.\n")

while True:

    question = input("Ask Question: ")

    if question.lower() == "exit":
        print("Program stopped.")
        break

    ask_question(question)




