from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

# -----------------------------
# App init
# -----------------------------
app = FastAPI(title="AI Knowledge Graph Backend")

# -----------------------------
# Load data for Semantic Search
# -----------------------------
movies = pd.read_csv("data/movies_metadata.csv", low_memory=False)
movies = movies[["id", "title", "overview"]].dropna().head(1000)
documents = movies.to_dict("records")

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(
    [doc["overview"] for doc in documents],
    show_progress_bar=True
)
embeddings = np.array(embeddings)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# -----------------------------
# Neo4j connection
# -----------------------------
NEO4J_URI = "neo4j+s://e27135de.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "WkmpufxtnWTdPav7XT1Ae9KD-_5H30FodCux9HlQLYY"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# -----------------------------
# Request model
# -----------------------------
class Query(BaseModel):
    query: str
    top_k: int = 5

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"status": "Backend running"}

# -----------------------------
# 1️⃣ Semantic Search API
# -----------------------------
@app.post("/semantic-search")
def semantic_search(payload: Query):
    query_vector = model.encode([payload.query])
    distances, indices = index.search(query_vector, payload.top_k)

    results = []
    for idx in indices[0]:
        results.append({
            "id": documents[idx]["id"],
            "title": documents[idx]["title"],
            "overview": documents[idx]["overview"]
        })

    return {
        "query": payload.query,
        "results": results
    }

# -----------------------------
# 2️⃣ RAG API
# -----------------------------
@app.post("/rag-query")
def rag_query(payload: Query):
    query_vector = model.encode([payload.query])
    distances, indices = index.search(query_vector, payload.top_k)

    retrieved_docs = []
    for idx in indices[0]:
        retrieved_docs.append({
            "title": documents[idx]["title"],
            "overview": documents[idx]["overview"]
        })

    # Build a better RAG-style answer
    answer = (
        f"Based on semantic understanding of the query "
        f"'{payload.query}', the following movies are relevant because "
        f"their storylines align with the theme:\n\n"
    )

    for doc in retrieved_docs:
        answer += f"- {doc['title']}: {doc['overview'][:180]}...\n"

    return {
        "query": payload.query,
        "answer": answer,
        "sources": [doc["title"] for doc in retrieved_docs]
    }

# -----------------------------
# 3️⃣ Neo4j Graph API
# -----------------------------
@app.get("/graph-data")
def graph_data():
    try:
        with driver.session() as session:
            result = session.run("""
            MATCH (a)-[r]->(b)
            WHERE a.name IS NOT NULL AND b.name IS NOT NULL
            RETURN a.name AS source, type(r) AS relation, b.name AS target
            LIMIT 50
            """)

            nodes = set()
            edges = []

            for row in result:
                source = str(row["source"])
                target = str(row["target"])

                nodes.add(source)
                nodes.add(target)

                edges.append({
                    "source": source,
                    "target": target,
                    "relation": row["relation"]
                })

            return {
                "nodes": [{"id": n, "label": n} for n in nodes],
                "edges": edges
            }

    except Exception as e:
        return {
            "nodes": [],
            "edges": [],
            "error": str(e)
        }

