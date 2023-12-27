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

import globalVar from "../../global.js";

const MonthlyAverageRatingsChart = (userName) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch data from the provided URL
    fetch(
      "http://127.0.0.1:8008/" + userName + "/monthly_average_rating"
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Extract the monthly average ratings from the response
        const monthlyRatings = data.monthly_average_ratings || [];

        // Transform the data into the desired format
        const transformed = monthlyRatings.map((rating) => ({
          month: `${rating.year}-${String(rating.month).padStart(2, "0")}`,
          averageRating: rating.average_rating.toFixed(1),
        }));

        // Set the transformed data in state
        setData(transformed);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }, []);
  return (
    <div>
      {" "}
      <div style={{ color: "white" }}>
        <h3>Artist Placement According to Number of Songs Released </h3>
      </div>
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
    </div>
  );
};

export default MonthlyAverageRatingsChart;
