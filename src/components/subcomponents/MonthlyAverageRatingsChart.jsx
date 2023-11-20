import { Colors } from "chart.js";
import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const MonthlyAverageRatingsChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("../../../data/ratings.json")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <>
      <h3 style={{ color: "white" }}> Monthly Average Rating</h3>
      <LineChart
        style={{ marginLeft: "10rem" }}
        width={500}
        height={300}
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="averageRating"
          stroke="#8884d8"
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </>
  );
};

export default MonthlyAverageRatingsChart;
