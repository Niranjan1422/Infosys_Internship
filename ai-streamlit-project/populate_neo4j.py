import pandas as pd
import ast
from neo4j import GraphDatabase

# -------------------------
# Neo4j connection
# -------------------------
NEO4J_URI = "neo4j+s://e27135de.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "WkmpufxtnWTdPav7XT1Ae9KD-_5H30FodCux9HlQLYY"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
    connection_timeout=30,
    max_connection_lifetime=60
)

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("data/movies_metadata.csv", low_memory=False)

df = df[["title", "genres"]].dropna().head(500)  
# limit for demo + safety

# -------------------------
# Helper function
# -------------------------
def create_movie_genre(tx, movie_title, genre_name):
    tx.run("""
        MERGE (m:Movie {name: $movie})
        MERGE (g:Genre {name: $genre})
        MERGE (m)-[:HAS_GENRE]->(g)
    """, movie=movie_title, genre=genre_name)

# -------------------------
# Populate graph
# -------------------------
BATCH_SIZE = 50

with driver.session() as session:
    batch = []

    for _, row in df.iterrows():
        try:
            genres = ast.literal_eval(row["genres"])
            for genre in genres:
                batch.append((row["title"], genre["name"]))

            if len(batch) >= BATCH_SIZE:
                session.execute_write(
                    lambda tx: [
                        create_movie_genre(tx, movie, genre)
                        for movie, genre in batch
                    ]
                )
                batch = []

        except Exception:
            continue

    # write remaining
    if batch:
        session.execute_write(
            lambda tx: [
                create_movie_genre(tx, movie, genre)
                for movie, genre in batch
            ]
        )

driver.close()

print("✅ Neo4j Knowledge Graph populated successfully")
