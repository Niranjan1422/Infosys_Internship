import streamlit as st
import requests
from pyvis.network import Network

st.set_page_config(layout="wide")
st.title("AI Knowledge Graph Dashboard")

BACKEND_URL = "http://127.0.0.1:8000"

# -------------------------
# Semantic Search
# -------------------------
st.header("🔍 Semantic Search")
query = st.text_input("Ask a question")

if st.button("Search"):
    res = requests.post(
        f"{BACKEND_URL}/semantic-search",
        json={"query": query, "top_k": 5}
    ).json()

    for r in res["results"]:
        st.subheader(r["title"])
        st.write(r["overview"])

# -------------------------
# RAG Answer
# -------------------------
st.header("🤖 RAG Answer")

if st.button("Get Answer"):
    res = requests.post(
        f"{BACKEND_URL}/rag-query",
        json={"query": query, "top_k": 3}
    ).json()

    st.success(res["answer"])

# -------------------------
# Knowledge Graph
# -------------------------
st.header("🧠 Knowledge Graph")

graph_response = requests.get(f"{BACKEND_URL}/graph-data")

if graph_response.status_code != 200:
    st.error("Knowledge Graph backend is not available.")
    st.stop()

graph = graph_response.json()


net = Network(height="500px", width="100%", bgcolor="white")

for node in graph.get("nodes", []):
    if node.get("id") is not None:
        net.add_node(str(node["id"]), label=str(node["label"]))

for edge in graph.get("edges", []):
    if edge.get("source") and edge.get("target"):
        net.add_edge(
            str(edge["source"]),
            str(edge["target"]),
            label=str(edge["relation"])
        )

net.save_graph("graph.html")
st.components.v1.html(open("graph.html").read(), height=550)
