import os
import json
import ast
import pandas as pd
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from ollama_service import generate_answer
from neo4j_service import create_graph

load_dotenv()

DATA_PATH = "../dataset"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

movies = pd.read_csv(f"{DATA_PATH}/movies_metadata.csv", low_memory=False)
credits = pd.read_csv(f"{DATA_PATH}/credits.csv")
keywords = pd.read_csv(f"{DATA_PATH}/keywords.csv")

movies = movies.drop_duplicates(subset=["id"])
movies["id"] = pd.to_numeric(movies["id"], errors="coerce")
movies = movies.dropna(subset=["id"])
movies["id"] = movies["id"].astype(int)
movies = movies.dropna(subset=["overview"])

metadata_map = movies.set_index("id").to_dict("index")


def safe_parse(x):
    try:
        return json.loads(x)
    except:
        try:
            return ast.literal_eval(x)
        except:
            return []


def rag_query(query):

    ranked_movies = []

    query_embedding = embedding_model.encode(query).tolist()
    pinecone_results = index.query(vector=query_embedding, top_k=30)

    for match in pinecone_results["matches"]:

        movie_id = int(match["id"])
        score = match["score"] * 2

        meta = metadata_map.get(movie_id)
        if not meta:
            continue

        title = meta.get("title")
        overview = meta.get("overview", "").lower()

        # 🔥 Genre Boost
        genres = [
            g.get("name", "").lower()
            for g in safe_parse(meta.get("genres", "[]"))
        ]

        if any(word.lower() in genres for word in query.lower().split()):
            score += 4

        # 🔥 Keyword Boost
        kw_row = keywords[keywords["id"] == movie_id]
        if not kw_row.empty:
            movie_keywords = [
                k.get("name", "").lower()
                for k in safe_parse(kw_row.iloc[0]["keywords"])
            ]
            if any(word.lower() in movie_keywords for word in query.lower().split()):
                score += 3

        ranked_movies.append({
            "movie_id": movie_id,
            "title": title,
            "final_score": round(score, 2)
        })

    ranked_movies = sorted(
        ranked_movies,
        key=lambda x: x["final_score"],
        reverse=True
    )[:8]

    graph_triples = []
    context_chunks = []

    for movie in ranked_movies:

        movie_id = movie["movie_id"]
        title = movie["title"]
        meta = metadata_map.get(movie_id)

        graph_triples.append({
            "source": query,
            "relation": "RELEVANT_TO_QUERY",
            "target": title
        })

        # GENRES
        for g in safe_parse(meta.get("genres", "[]"))[:3]:
            graph_triples.append({
                "source": title,
                "relation": "HAS_GENRE",
                "target": g.get("name")
            })

        # KEYWORDS
        kw_row = keywords[keywords["id"] == movie_id]
        if not kw_row.empty:
            for kw in safe_parse(kw_row.iloc[0]["keywords"])[:3]:
                graph_triples.append({
                    "source": title,
                    "relation": "HAS_KEYWORD",
                    "target": kw.get("name")
                })

        # ACTORS & DIRECTOR
        credit_row = credits[credits["id"] == movie_id]
        if not credit_row.empty:
            cast_list = safe_parse(credit_row.iloc[0]["cast"])
            crew_list = safe_parse(credit_row.iloc[0]["crew"])

            for actor in cast_list[:3]:
                graph_triples.append({
                    "source": title,
                    "relation": "HAS_ACTOR",
                    "target": actor.get("name")
                })

            for crew in crew_list:
                if crew.get("job") == "Director":
                    graph_triples.append({
                        "source": title,
                        "relation": "DIRECTED_BY",
                        "target": crew.get("name")
                    })
                    break

        context_chunks.append(meta.get("overview", "")[:400])

    create_graph(graph_triples)

    context = "\n\n".join(context_chunks)
    answer = generate_answer(query, context)

    return {
        "query": query,
        "ranked_movies": ranked_movies,
        "graph_triples": graph_triples,
        "answer": answer
    }