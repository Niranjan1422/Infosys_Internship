import React, { useState, useRef } from "react";
import axios from "axios";
import ForceGraph2D from "react-force-graph-2d";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

function App() {

  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [stats, setStats] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const graphRef = useRef();

  const COLORS = ["#3b82f6","#10b981","#f59e0b","#ef4444","#a855f7","#22d3ee"];

  const nodeColor = (group) => {
    switch(group) {
      case "query": return "#ffffff";
      case "movie": return "#3b82f6";
      case "genre": return "#10b981";
      case "actor": return "#f59e0b";
      case "director": return "#ef4444";
      case "keyword": return "#a855f7";
      default: return "#94a3b8";
    }
  };

  const handleSearch = async () => {

    if (!query.trim()) return;

    try {

      const ragRes = await axios.post("http://127.0.0.1:8000/rag-query", { query });
      setResult(ragRes.data);

      const graphRes = await axios.post("http://127.0.0.1:8000/graph", { query });
      setGraphData(graphRes.data);

      const statRes = await axios.post("http://127.0.0.1:8000/query-stats", { query });
      setStats(statRes.data);

      const metricRes = await axios.get("http://127.0.0.1:8000/metrics");
      setMetrics(metricRes.data);

      setTimeout(() => {
        if (graphRef.current) graphRef.current.zoomToFit(500);
      }, 1000);

    } catch (err) {
      console.error("Search Error:", err);
    }
  };

  const relationDistribution = result
    ? Object.entries(
        result.graph_triples.reduce((acc, cur) => {
          acc[cur.relation] = (acc[cur.relation] || 0) + 1;
          return acc;
        }, {})
      ).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div style={{ background:"#0b1220", minHeight:"100vh", padding:30, color:"white" }}>

      <h1 style={{
        textAlign:"center",
        fontSize:38,
        fontWeight:"bold",
        color:"#38bdf8",
        marginBottom:30
      }}>
        AI Based Knowledge Graph for Enterprise Intelligence
      </h1>

      {stats && metrics && (
        <div style={{ display:"flex", justifyContent:"space-around", marginBottom:30 }}>
          <StatCard title="Total Nodes" value={stats.total_nodes} color="#3b82f6"/>
          <StatCard title="Total Relationships" value={stats.total_relationships} color="#10b981"/>
          <StatCard title="CPU Usage" value={`${metrics.cpu_usage}%`} color="#f59e0b"/>
          <StatCard title="Memory Usage" value={`${metrics.memory_usage}%`} color="#ef4444"/>
        </div>
      )}

      <div style={{ textAlign:"center", marginBottom:40 }}>
        <input
          value={query}
          onChange={(e)=>setQuery(e.target.value)}
          placeholder="Enter enterprise query..."
          style={{
            padding:15,
            width:500,
            fontSize:16,
            borderRadius:8,
            border:"none"
          }}
        />
        <button
          onClick={handleSearch}
          style={{
            padding:15,
            marginLeft:10,
            fontSize:16,
            borderRadius:8,
            cursor:"pointer",
            background:"#22c55e",
            color:"white",
            border:"none"
          }}
        >
          Search
        </button>
      </div>

      {result && (
        <>
          <Section title="AI Insight" color="#f472b6">
            <p style={{ lineHeight:1.7 }}>{result.answer}</p>
          </Section>

          <Section title="Top Ranked Movies" color="#22d3ee">
            <ul>
              {result.ranked_movies.map((m,i)=>(
                <li key={i}>{m.title} (Score: {m.final_score})</li>
              ))}
            </ul>
          </Section>

          <Section title="Relation Distribution" color="#a78bfa">
            <PieChart width={450} height={300}>
              <Pie data={relationDistribution} dataKey="value" nameKey="name" outerRadius={110}>
                {relationDistribution.map((entry,index)=>(
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </Section>

          <Section title="Graph Relationships" color="#facc15">
            {result.graph_triples.map((r,i)=>(
              <div key={i}>{r.source} → {r.relation} → {r.target}</div>
            ))}
          </Section>
        </>
      )}

      <h2 style={{ textAlign:"center", marginTop:40, color:"#f87171" }}>
        Interactive Knowledge Graph
      </h2>

      <ForceGraph2D
  ref={graphRef}
  graphData={graphData}
  width={window.innerWidth - 60}
  height={750}
  backgroundColor="#0b1220"
  linkDirectionalArrowLength={6}
  linkDirectionalArrowRelPos={1}
  linkColor={() => "#64748b"}
  cooldownTicks={200}
  d3VelocityDecay={0.25}
  onEngineStop={() => graphRef.current.zoomToFit(600)}

  nodeCanvasObject={(node, ctx, globalScale) => {

    const radius = node.group === "query" ? 22 : 8;

    // Draw node
    ctx.beginPath();
    ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = nodeColor(node.group);
    ctx.fill();

    // Show label ONLY if zoomed enough
    if (globalScale > 1.5) {
      const label = node.id;
      const fontSize = 14 / globalScale;
      ctx.font = `${fontSize}px Sans-Serif`;
      ctx.fillStyle = "#ffffff";
      ctx.fillText(label, node.x + radius + 4, node.y + 4);
    }
  }}

  linkCanvasObjectMode={() => "after"}
  linkCanvasObject={(link, ctx, globalScale) => {

    // Show relationship text ONLY when zoomed
    if (globalScale > 2) {
      const start = link.source;
      const end = link.target;
      if (!start || !end) return;

      const midX = start.x + (end.x - start.x) / 2;
      const midY = start.y + (end.y - start.y) / 2;

      const fontSize = 10 / globalScale;
      ctx.font = `${fontSize}px Sans-Serif`;
      ctx.fillStyle = "#94a3b8";
      ctx.fillText(link.label, midX, midY);
    }
  }}

  d3Force="charge"
  d3ForceConfig={{
    charge: { strength: -500 },
    link: { distance: 160 },
    collide: { radius: 30 }
  }}

  nodeLabel={(node) => `${node.id} (${node.group})`}
  linkLabel={(link) => link.label}
/>

    </div>
  );
}

function StatCard({title,value,color}) {
  return (
    <div style={{
      background:"#111827",
      padding:20,
      borderRadius:12,
      width:220,
      textAlign:"center",
      border:`2px solid ${color}`
    }}>
      <h3 style={{ color }}>{title}</h3>
      <p style={{ fontSize:22 }}>{value}</p>
    </div>
  );
}

function Section({title,color,children}) {
  return (
    <div style={{
      background:"#1e293b",
      padding:25,
      borderRadius:12,
      marginBottom:30
    }}>
      <h2 style={{ color }}>{title}</h2>
      {children}
    </div>
  );
}

export default App;