# #Infosys_SpringBoard_Internship_Project
---------------------------------------------------------------------------------------------

# Enterprise Knowledge Graph & RAG-Based Intelligent Search Platform

# 📌 Overview

This project was developed during my internship to design and implement an Enterprise Knowledge Graph powered by LLM-based Entity Extraction, Semantic Search, and Retrieval-Augmented Generation (RAG).

The system enables intelligent search and graph-based exploration of enterprise data using modern AI pipelines.

---------------------------------------------------------------------------------------------

# 🚀 Milestones


🔹 Milestone 1: Data Ingestion & Schema Design 

Built ingestion pipelines

Connected enterprise datasets

Designed Neo4j graph schema


🔹 Milestone 2: Entity Extraction & Graph Building 

Applied LLM-based Named Entity Recognition

Extracted relationships

Stored graph in Neo4j

Validated graph structure


🔹 Milestone 3: Semantic Search & RAG 

Generated embeddings

Integrated FAISS / Pinecone

Built semantic search pipeline

Implemented Retrieval-Augmented Generation


🔹 Milestone 4: Dashboard & Deployment 

Built interactive React dashboard

Graph visualization UI

API integration

Full system deployment 

---------------------------------------------------------------------------------------------

# 🏗 Project Structure

backend/                → FastAPI backend, graph & RAG services

milestone4-dashboard/   → React frontend dashboard

notebooks/              → Milestone research notebooks

---------------------------------------------------------------------------------------------
# 🛠 Tech Stack

Python

FastAPI

Neo4j

FAISS / Pinecone

Ollama / LLM APIs

React.js

Node.js

---------------------------------------------------------------------------------------------
# 📂 Dataset Information

⚠️ Dataset is NOT included in this repository due to size constraints.

Please download the dataset separately from https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset and place it inside:

backend/dataset/

Make sure required CSV files are present before running ingestion pipelines.

---------------------------------------------------------------------------------------------
# ⚙️ Backend Setup 

cd backend

pip install -r requirements.txt

uvicorn app:app --reload

# ⚙️ Frontend Setup


cd milestone4-dashboard

npm install

npm start

---------------------------------------------------------------------------------------------
# 🔐 Environment Variables

Create a .env file inside backend/ and configure:

PINECONE_API_KEY=xyz

PINECONE_INDEX=xyz

NEO4J_URI=xyz

NEO4J_USERNAME=xyz

NEO4J_PASSWORD=xyz

OLLAMA_MODEL=xyz


---------------------------------------------------------------------------------------------

# 🚀 Future Scope: Enterprise-Grade AI & Retrieval Upgrades

This section outlines planned architectural improvements to enhance scalability, retrieval quality, enterprise readiness, and system robustness.
_____________________________________________________________________________________________

# 1️⃣ LLM Inference Layer Upgrade

✅ Current Implementation
-
LLM inference is performed locally using:
•	Ollama
•	Open-source models (e.g., Mistral, Phi)

Why This Was Chosen
-
•	Fully free and offline
•	No API cost
•	Easy local experimentation
•	No dependency on external providers

Current Limitations
-
•	Limited scalability (runs on local hardware)
•	Hardware-dependent performance
•	No auto-scaling
•	Limited monitoring and logging
•	Lower reasoning performance compared to frontier APIs
_____________________________________________________________________________________________

🔄 Proposed Future Upgrade
-

Migrate to managed cloud-based inference via:
•	Vertex AI (Gemini models)

Why Vertex AI
-
•	Enterprise-grade infrastructure
•	Auto-scaling endpoints
•	Production-level SLAs
•	Built-in monitoring and logging
•	Secure service account authentication
•	Seamless integration with Google Cloud ecosystem

Why Not Continue with Ollama in Production
-
•	Cannot scale dynamically
•	Requires dedicated GPU/CPU server
•	Not suitable for high concurrent user traffic
•	Infrastructure maintenance overhead

Why Vertex AI Instead of Other Cloud LLMs
-
Option ||	Reason Not Primary Choice
-
Direct OpenAI GPT || Strong, but less enterprise integration if deploying on GCP
Self-hosted models on VM || Requires GPU provisioning & DevOps overhead
Anthropic API	|| Similar benefits, but Vertex integrates natively with GCP

Vertex AI is preferred if deploying on Google Cloud infrastructure.
_____________________________________________________________________________________________

# 2️⃣ Embedding Model Upgrade

✅ Current Implementation
-
Local embeddings using SentenceTransformers.

Why This Was Chosen
-
•	Free
•	No external API calls
•	Simple integration
•	Good baseline semantic performance

Current Limitations
-
•	Lower retrieval accuracy compared to commercial embedding APIs
•	Limited multilingual optimization
•	No continuous model improvement
•	No retrieval-optimized tuning
_____________________________________________________________________________________________

🔄 Proposed Future Upgrade
-
Option A
-
OpenAI Embeddings

Option B
-
Voyage AI
_____________________________________________________________________________________________
Why Upgrade Embeddings
-
•	Higher semantic accuracy
•	Better recall in RAG pipelines
•	Optimized for retrieval tasks
•	Improved domain adaptation
•	Continuous model updates from provider
_____________________________________________________________________________________________
Why OpenAI Small Embeddings
-
•	Cost-efficient
•	High quality
•	Well-documented
•	Stable API ecosystem
_____________________________________________________________________________________________
Why Voyage AI
-
•	Designed specifically for retrieval
•	Often outperforms general-purpose embeddings in RAG systems
•	Better for large-scale search-heavy architectures
_____________________________________________________________________________________________
Why Not Keep Local Embeddings in Production
-
•	Quality ceiling is lower
•	No guaranteed consistency across deployments
•	Harder to scale and optimize
•	Manual model version control required
_____________________________________________________________________________________________

# 3️⃣ Retrieval Strategy Upgrade

✅ Current Implementation
-
Dense vector retrieval using:
•	Pinecone

Why This Was Chosen
-
•	Managed vector storage
•	Free starter tier
•	Fast similarity search
•	Easy FastAPI integration
_____________________________________________________________________________________________

🔄 Future Upgrade: Hybrid Search
-
Combine:
•	Dense semantic search (Pinecone)
•	Sparse keyword search (BM25)

Lightweight implementation via:
•	rank-bm25 (Python-based sparse retrieval)
_____________________________________________________________________________________________
Why Hybrid Search
-
•	Improves precision for exact terms (e.g., compliance codes, section numbers)
•	Reduces failure in numeric or identifier-based queries
•	Balances semantic meaning + exact matching
•	Improves overall recall and MRR score
_____________________________________________________________________________________________
Why Not Use Heavy Search Engines
-

Option || Reason Not Chosen
-
Elasticsearch	|| RAM-heavy, complex setup
Self-managed OpenSearch	|| Infrastructure overhead

Hybrid Python-based solution keeps deployment lightweight.
_____________________________________________________________________________________________

# 4️⃣ Query Routing & Agentic Orchestration

✅ Current Implementation
-
Single RAG pipeline (Vector → LLM)

Limitation
-
All queries treated the same way.
_____________________________________________________________________________________________

🔄 Future Upgrade
-
Introduce intelligent routing layer:
•	Normal RAG
•	Graph RAG
•	Agentic multi-step RAG

Using orchestration frameworks such as:
•	LangChain
•	LlamaIndex
•	LangGraph
_____________________________________________________________________________________________
Why Add Routing
-
Different queries require different reasoning strategies:
•	Factual lookup → Vector RAG
•	Relationship reasoning → Graph RAG
•	Multi-step comparison → Agentic RAG

Routing improves:
•	Accuracy
•	Efficiency
•	Response reliability
_____________________________________________________________________________________________
Why Not Keep Single Pipeline
-
•	Inefficient for graph-heavy queries
•	Cannot support multi-step reasoning
•	Lower reasoning flexibility
_____________________________________________________________________________________________

# 5️⃣ Graph Intelligence Expansion

✅ Current Implementation
-
Relationship modeling using:
•	Neo4j

Purpose
-
•	Store structured relationships
•	Execute Cypher queries
_____________________________________________________________________________________________
🔄 Future Upgrade
-
Integrate graph reasoning inside agentic workflows.

Why
-
•	Allows LLM to dynamically query graph
•	Enables tool-based reasoning
•	Supports cross-database inference
_____________________________________________________________________________________________

# 6️⃣ Advanced Chunking Strategy

✅ Current Implementation
-
Fixed-size token chunking.

Limitation
-
•	Breaks semantic boundaries
•	May reduce retrieval accuracy
_____________________________________________________________________________________________
🔄 Future Upgrade
-
•	Semantic chunking
•	Parent–child chunking
•	Contextual metadata enrichment

Why
-
•	Preserves logical structure
•	Improves retrieval precision
•	Enables hierarchical reasoning
_____________________________________________________________________________________________

# 7️⃣ Retrieval Evaluation Framework

✅ Current Implementation
-
Manual result inspection.
_____________________________________________________________________________________________
🔄 Future Upgrade
-
Automated evaluation using:
•	RAGAS

Metrics:
•	MRR (Mean Reciprocal Rank)
•	Recall@K
•	Precision@K
•	Faithfulness
_____________________________________________________________________________________________
Why Add Evaluation Layer
-
•	Enables scientific benchmarking
•	Ensures production reliability
•	Measures improvement after upgrades
_____________________________________________________________________________________________

# 8️⃣ Memory Architecture Expansion

✅ Current Implementation
-
Session-based memory.
_____________________________________________________________________________________________
🔄 Future Upgrade
-
Short-Term Memory
-
•	Redis-based session storage

Long-Term Memory
-
•	Persistent user interaction memory
•	Vector-based semantic memory
•	Graph-based relational memory
_____________________________________________________________________________________________
Why Add Memory Layers
-
•	Personalized responses
•	Context continuity
•	Organization-level intelligence
_____________________________________________________________________________________________

# 🏗️ Final Future Architecture (Enterprise Target)

Planned architecture:

•	Frontend: Vercel

•	Backend: Render

•	LLM: Vertex AI

•	Embeddings: OpenAI / Voyage

•	Vector DB: Pinecone

•	Graph DB: Neo4j

•	Hybrid Search: Dense + BM25

•	Agentic Routing Layer

•	Evaluation Metrics

•	Multi-layer Memory System
_____________________________________________________________________________________________

# 🎯 Overall Goal of Future Scope

These upgrades will transition the system from:
Academic/Prototype RAG Systemm to
Enterprise-Ready AI Knowledge Graph & Intelligent Retrieval Platform
with improved scalability, reliability, reasoning depth, and retrieval performance.

---------------------------------------------------------------------------------------------
# 📜 License

This project is licensed under the MIT License.

# 👤 Author

Niranjan Patil

Infosys Internship Project
