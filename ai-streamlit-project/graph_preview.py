import networkx as nx
import plotly.graph_objects as go

G = nx.Graph()

edges = [
    ("The Matrix", "Science Fiction"),
    ("Inception", "Science Fiction"),
    ("Interstellar", "Science Fiction"),
    ("The Matrix", "Action"),
    ("Inception", "Thriller")
]

G.add_edges_from(edges)

pos = nx.spring_layout(G, seed=42)

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    mode="lines",
    line=dict(width=1),
    hoverinfo="none"
)

node_x = []
node_y = []
node_text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    textposition="top center",
    marker=dict(size=20)
)

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title="Milestone 3 – Knowledge Graph Visualization (Plotly)",
        showlegend=False
    )
)

fig.show()
