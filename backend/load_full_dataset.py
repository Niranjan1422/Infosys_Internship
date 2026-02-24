# backend/load_full_dataset.py

import pandas as pd
import json
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

# Load CSVs
movies = pd.read_csv("movies_metadata.csv", low_memory=False)
credits = pd.read_csv("credits.csv")
keywords = pd.read_csv("keywords.csv")
ratings = pd.read_csv("ratings.csv")

# Clean dataset
movies = movies[["id", "title", "overview", "genres"]].dropna()

def insert_movie(tx, movie):
    tx.run("""
        MERGE (m:Movie {id: $id})
        SET m.title = $title,
            m.overview = $overview
    """, id=str(movie["id"]),
         title=movie["title"],
         overview=movie["overview"])

def insert_genres(tx, movie_id, genres):
    for genre in genres:
        tx.run("""
            MATCH (m:Movie {id: $movie_id})
            MERGE (g:Genre {name: $name})
            MERGE (m)-[:HAS_GENRE]->(g)
        """, movie_id=str(movie_id), name=genre["name"])

def insert_credits(tx, movie_id, cast_json):
    cast = json.loads(cast_json)
    for actor in cast[:5]:
        tx.run("""
            MATCH (m:Movie {id: $movie_id})
            MERGE (a:Actor {name: $name})
            MERGE (m)-[:ACTED_IN]->(a)
        """, movie_id=str(movie_id), name=actor["name"])

def insert_keywords(tx, movie_id, keyword_json):
    keys = json.loads(keyword_json)
    for key in keys:
        tx.run("""
            MATCH (m:Movie {id: $movie_id})
            MERGE (k:Keyword {name: $name})
            MERGE (m)-[:HAS_KEYWORD]->(k)
        """, movie_id=str(movie_id), name=key["name"])

def insert_rating(tx, movie_id, avg_rating):
    tx.run("""
        MATCH (m:Movie {id: $movie_id})
        SET m.avg_rating = $rating
    """, movie_id=str(movie_id), rating=avg_rating)

with driver.session() as session:
    for _, movie in movies.iterrows():
        session.execute_write(insert_movie, movie)

        if pd.notna(movie["genres"]):
            session.execute_write(
                insert_genres,
                movie["id"],
                json.loads(movie["genres"])
            )

        credit_row = credits[credits["id"] == int(movie["id"])]
        if not credit_row.empty:
            session.execute_write(
                insert_credits,
                movie["id"],
                credit_row.iloc[0]["cast"]
            )

        keyword_row = keywords[keywords["id"] == int(movie["id"])]
        if not keyword_row.empty:
            session.execute_write(
                insert_keywords,
                movie["id"],
                keyword_row.iloc[0]["keywords"]
            )

print("✅ Enterprise Graph Built Successfully")