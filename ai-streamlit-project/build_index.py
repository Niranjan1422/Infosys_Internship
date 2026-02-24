import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/movies_metadata.csv", low_memory=False)
df = df[["title", "overview"]].dropna().head(500)

texts = df["overview"].tolist()

# -----------------------------
# Generate embeddings
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings)

print("Embedding shape:", embeddings.shape)

# -----------------------------
# Build FAISS index
# -----------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("FAISS index size:", index.ntotal)

# -----------------------------
# Save index + metadata
# -----------------------------
faiss.write_index(index, "movie_index.faiss")

with open("documents.pkl", "wb") as f:
    pickle.dump(df.to_dict("records"), f)

print("✅ FAISS index and documents saved")
