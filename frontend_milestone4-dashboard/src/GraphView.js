import React, { useEffect, useRef } from "react";
import Sigma from "sigma";
import Graph from "graphology";
import forceAtlas2 from "graphology-layout-forceatlas2";

const GraphView = ({ data }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!data || !data.nodes) return;

    const graph = new Graph();

    data.nodes.forEach(node => {
      if (!graph.hasNode(node.id)) {
        graph.addNode(node.id, {
          label: node.label,
          size: node.size || 5,
          color: "#6366f1"
        });
      }
    });

    data.edges.forEach((edge, i) => {
      graph.addEdge(edge.source, edge.target, {
        label: edge.label,
        size: 1,
        color: "#ccc"
      });
    });

    forceAtlas2.assign(graph, { iterations: 50 });

    const renderer = new Sigma(graph, containerRef.current);

    return () => renderer.kill();
  }, [data]);

  return <div ref={containerRef} style={{ height: "600px" }} />;
};

export default GraphView;