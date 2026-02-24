import React from "react";
import ForceGraph2D from "react-force-graph";

const data = {
  nodes: [
    { id: "The Matrix" },
    { id: "Science Fiction" },
    { id: "Action" }
  ],
  links: [
    { source: "The Matrix", target: "Science Fiction" },
    { source: "The Matrix", target: "Action" }
  ]
};

export default function Graph() {
  return <ForceGraph2D graphData={data} />;
}
