from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def create_graph(triples):

    with driver.session() as session:

        for triple in triples:

            source = triple["source"]
            relation = triple["relation"]
            target = triple["target"]

            if relation == "RELEVANT_TO_QUERY":

                session.run("""
                MERGE (q:Query {name: $source})
                MERGE (m:Movie {title: $target})
                MERGE (q)-[:RELEVANT_TO_QUERY]->(m)
                """, source=source, target=target)

            else:

                session.run(f"""
                MERGE (m:Movie {{title: $source}})
                MERGE (e:Entity {{name: $target}})
                MERGE (m)-[:{relation}]->(e)
                """, source=source, target=target)


def get_subgraph(search_query):

    with driver.session() as session:

        result = session.run("""
        MATCH (q:Query {name: $qname})-[r]->(m:Movie)
        OPTIONAL MATCH (m)-[r2]->(e)
        RETURN q.name AS query_name,
               m.title AS movie_title,
               type(r) AS rel1,
               e.name AS entity_name,
               type(r2) AS rel2
        """, qname=search_query)

        nodes = {}
        links = []

        for record in result:

            query_name = record["query_name"]
            movie_title = record["movie_title"]
            entity_name = record["entity_name"]
            rel1 = record["rel1"]
            rel2 = record["rel2"]

            # Query Node
            if query_name and query_name not in nodes:
                nodes[query_name] = {
                    "id": query_name,
                    "group": "query"
                }

            # Movie Node
            if movie_title and movie_title not in nodes:
                nodes[movie_title] = {
                    "id": movie_title,
                    "group": "movie"
                }

            # Query → Movie Link
            if query_name and movie_title:
                links.append({
                    "source": query_name,
                    "target": movie_title,
                    "label": rel1
                })

            # Entity Node
            if entity_name:
                group = "entity"

                if rel2 == "HAS_GENRE":
                    group = "genre"
                elif rel2 == "HAS_ACTOR":
                    group = "actor"
                elif rel2 == "DIRECTED_BY":
                    group = "director"
                elif rel2 == "HAS_KEYWORD":
                    group = "keyword"

                if entity_name not in nodes:
                    nodes[entity_name] = {
                        "id": entity_name,
                        "group": group
                    }

                links.append({
                    "source": movie_title,
                    "target": entity_name,
                    "label": rel2
                })

        return {
            "nodes": list(nodes.values()),
            "links": links
        }


def get_query_stats(query_name):

    with driver.session() as session:

        result = session.run("""
        MATCH (q:Query {name:$name})-[r1]->(m:Movie)
        OPTIONAL MATCH (m)-[r2]->()
        RETURN count(DISTINCT q) + count(DISTINCT m) + count(DISTINCT r2) AS total_nodes,
               count(DISTINCT r1) + count(DISTINCT r2) AS total_relationships
        """, name=query_name)

        record = result.single()

        return {
            "total_nodes": record["total_nodes"] if record else 0,
            "total_relationships": record["total_relationships"] if record else 0
        }