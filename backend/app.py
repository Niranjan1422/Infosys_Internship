from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psutil

from graph_rag import rag_query
from neo4j_service import get_subgraph, get_query_stats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


@app.post("/rag-query")
def rag(data: QueryRequest):
    return rag_query(data.query)


@app.post("/graph")
def graph(data: QueryRequest):
    return get_subgraph(data.query)


@app.post("/query-stats")
def query_stats(data: QueryRequest):
    return get_query_stats(data.query)


@app.get("/metrics")
def metrics():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent
    }