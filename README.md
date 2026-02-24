#Infosys_SpringBoard_Internship_Project

Enterprise Knowledge Graph & RAG-Based Intelligent Search Platform

📌 Overview

This project was developed during my internship to design and implement an Enterprise Knowledge Graph powered by LLM-based Entity Extraction, Semantic Search, and Retrieval-Augmented Generation (RAG).

The system enables intelligent search and graph-based exploration of enterprise data using modern AI pipelines.

---------------------------------------------------------------------------------------------

🚀 Milestones
🔹 Milestone 1: Data Ingestion & Schema Design (Weeks 1–2)

Built ingestion pipelines

Connected enterprise datasets

Designed Neo4j graph schema

🔹 Milestone 2: Entity Extraction & Graph Building (Weeks 3–4)

Applied LLM-based Named Entity Recognition

Extracted relationships

Stored graph in Neo4j

Validated graph structure

🔹 Milestone 3: Semantic Search & RAG (Weeks 5–6)

Generated embeddings

Integrated FAISS / Pinecone

Built semantic search pipeline

Implemented Retrieval-Augmented Generation

🔹 Milestone 4: Dashboard & Deployment (Weeks 7–8)

Built interactive React dashboard

Graph visualization UI

API integration

---------------------------------------------------------------------------------------------
Full system deployment =

🏗 Project Structure
backend/                → FastAPI backend, graph & RAG services
milestone4-dashboard/   → React frontend dashboard
notebooks/              → Milestone research notebooks

---------------------------------------------------------------------------------------------
🛠 Tech Stack

Python

FastAPI

Neo4j

FAISS / Pinecone

Ollama / LLM APIs

React.js

Node.js

---------------------------------------------------------------------------------------------
📂 Dataset Information

⚠️ Dataset is NOT included in this repository due to size constraints.

Please download the dataset separately from https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset and place it inside:

backend/dataset/

Make sure required CSV files are present before running ingestion pipelines.

---------------------------------------------------------------------------------------------
⚙️ Backend Setup = 
cd backend

pip install -r requirements.txt

uvicorn app:app --reload

⚙️ Frontend Setup = 
cd milestone4-dashboard
npm install
npm start

---------------------------------------------------------------------------------------------
🔐 Environment Variables

Create a .env file inside backend/ and configure:

NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=
OPENAI_API_KEY=

---------------------------------------------------------------------------------------------
📜 License

This project is licensed under the MIT License.

👤 Author

Niranjan Patil
Infosys Internship Project
