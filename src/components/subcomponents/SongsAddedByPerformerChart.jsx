import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const SongsAddedByPerformerChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("../../../data/songsByPerformer.json")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h3 style={{ color: "white" }}>
        {" "}
        Artist Placement According to Number of Songs Released{" "}
      </h3>
      <BarChart
        style={{ marginLeft: "10rem" }}
        width={500}
        height={300}
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="performer" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="songsAdded" fill="#82ca9d" />
      </BarChart>
    </div>
  );
};

export default SongsAddedByPerformerChart;
