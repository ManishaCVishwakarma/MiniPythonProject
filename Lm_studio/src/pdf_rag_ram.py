import requests
import numpy as np
from pypdf import PdfReader

# -------- LM Studio API --------
EMBED_URL = "http://192.168.31.39:1234/v1/embeddings"
CHAT_URL = "http://192.168.31.39:1234/v1/chat/completions"

EMBED_MODEL = "text-embedding-all-minilm-l6-v2-embedding"
LLM_MODEL = "google/gemma-3-1b"

# -------- PDF PATH --------
pdf_path = "D:\\PythonCoding\\Intership Note\\Introduction to DBMS.pdf"

print("Reading PDF...")

reader = PdfReader(pdf_path)

text = ""
for page in reader.pages:
    content = page.extract_text()
    if content:
        text += content

# -------- Split Text --------
chunk_size = 500
chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i+chunk_size])

print("Total chunks:", len(chunks))

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


# -------- Function to Ask Question --------
def ask_question(question):

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

    best_index = scores.index(max(scores))
    context = chunks[best_index]

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        CHAT_URL,
        json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]

    print("\nQuestion:", question)
    print("\nAnswer:\n", answer)
    print("\n----------------------------\n")


# -------- First Fixed Question --------
first_question = "What is DBMS?"
ask_question(first_question)


print("Now you can ask your own questions.")
print("Type 'exit' to stop.\n")

# -------- Continuous Questions --------
while True:

    question = input("Ask Question: ")

    if question.lower() == "exit":
        print("Program stopped.")
        break

    ask_question(question)