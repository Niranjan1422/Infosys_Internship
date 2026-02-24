🧠 AI-Based Knowledge Graph with Graph-Aware RAG
-

 Project Overview
 -

This project implements a Graph-Aware Retrieval-Augmented Generation (RAG) system that combines:

🔎 Semantic Search using Sentence Transformers

⚡ Fast Approximate Nearest Neighbor Search using FAISS

🗂 Knowledge Graph using Neo4j

🚀 API Layer using FastAPI

📊 Interactive Interface using Streamlit


The system enables intelligent, meaning-based retrieval over a structured knowledge graph and generates grounded responses by combining semantic and relational context.

--------------------------------------------

🎯 Objective 
-

The objective of this milestone is to:

Implement semantic search over unstructured data

Integrate vector retrieval with graph filtering

Build a graph-aware RAG pipeline

Reduce hallucinations through grounded responses

Prepare backend APIs for dashboard integration (Milestone 4)



--------------------------------------------

🏗 System Architecture
-

User Query (Streamlit UI)
        ↓
Sentence Transformer (Embedding)
        ↓
FAISS Vector Search
        ↓
Retrieve Relevant Entity IDs
        ↓
Neo4j Graph Filtering
        ↓
Combine Semantic + Graph Context
        ↓
Generate Grounded RAG Response


--------------------------------------------

🛠 Technologies Used
-

Component || Technology ||	Purpose
-

Embedding Model || SentenceTransformers || Convert text to dense vectors


Vector Search || FAISS || Fast ANN similarity search


Graph Database || Neo4j || Structured knowledge graph


Backend API || FastAPI || Expose RAG endpoints


UI || Streamlit || Interactive dashboard


Language || Python || Core implementation



--------------------------------------------

🔍 How the System Works
-

1️⃣ Semantic Embedding

Movie descriptions and metadata are converted into vector embeddings using:

all-MiniLM-L6-v2

These embeddings capture contextual meaning rather than exact words.


---

2️⃣ Vector Storage (FAISS)

The embeddings are stored in FAISS, which provides:

Efficient Approximate Nearest Neighbor (ANN) search

Fast local similarity lookup

Low-latency retrieval for prototyping



---

3️⃣ Query Processing

When a user enters a natural language query:

1. Query is converted into an embedding.


2. FAISS retrieves the most semantically similar vectors.


3. Relevant entity IDs are extracted.




---

4️⃣ Graph Filtering (Neo4j)

The retrieved entity IDs are passed to Neo4j.

The system extracts structured relationships such as:

HAS_GENRE

HAS_ACTOR

DIRECTED_BY

RELATED_TO


This step adds relational reasoning to the pipeline.


---

5️⃣ Graph-Aware RAG Response

The final response combines:

Semantic context (vector retrieval)

Structured graph triples (Neo4j)


This ensures responses are grounded in actual data and reduces hallucination.


---

🧪 Why FAISS Instead of Pinecone?
-

FAISS was selected because:

It is suitable for local prototyping

It provides efficient ANN search

It does not require cloud infrastructure

Milestone 3 focuses on functionality, not scaling


For enterprise-scale deployment, Pinecone would be used instead.


--------------------------------------------

🔐 How the System Reduces Hallucination
-

The RAG pipeline restricts generation to:

Retrieved semantic documents

Verified Neo4j graph relationships


The model does not generate responses beyond retrieved data, ensuring grounded outputs.


--------------------------------------------

⚙ Installation & Setup
-

1️⃣ Clone Repository

git clone https://github.com/yourusername/AI_Knowledge_Graph.git
cd AI_Knowledge_Graph


---

2️⃣ Create Virtual Environment

python -m venv kg_env
kg_env\Scripts\activate  # Windows


---

3️⃣ Install Dependencies

pip install -r requirements.txt


---

4️⃣ Run Neo4j

Ensure Neo4j is running locally:

bolt://localhost:7687

Update credentials in .env.


---

5️⃣ Build FAISS Index

Run the dataset loading script:

python load_full_dataset.py

This generates embeddings and builds the FAISS index.


---

6️⃣ Start FastAPI Backend

uvicorn app:app --reload

Backend runs at:

http://127.0.0.1:8000


---

7️⃣ Run Streamlit App


streamlit run streamlit_app.py


App opens at:


http://localhost:8501


---

📊 Features Implemented

✔ Semantic similarity search
✔ Vector-based retrieval
✔ Graph filtering with Neo4j
✔ Hybrid RAG pipeline
✔ Reduced hallucination
✔ API integration
✔ Dashboard-ready architecture


---

📈 Scalability Plan (Future Scope)
-

To scale this system:

Replace FAISS with Pinecone

Deploy FastAPI using Docker

Use Neo4j Aura for managed cloud graph

Add caching layer

Implement async request handling

Deploy on Kubernetes for horizontal scaling



---

🧠 Key Learning Outcomes
-

Implemented ANN vector search

Integrated vector DB with graph DB

Built hybrid RAG pipeline

Reduced hallucination via grounding

Designed scalable AI architecture



---

🚀 Milestone Transition
-

This backend is fully prepared for:

Interactive Dashboard (Milestone 4)

Deployment & Scaling

Enterprise Intelligence Extensions



--------------------------------------------

👨‍💻 Author
-

Niranjan Patil
