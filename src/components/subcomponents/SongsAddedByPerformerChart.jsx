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
import globalVar from "../../global.js";
const SongsAddedByPerformerChart = (userName) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch data from the provided URL
    fetch("http://127.0.0.1:8008/" + userName + "/artist_song_count")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Transform the fetched data into the desired format
        const transformed = data.map((artist) => ({
          performer: artist.artist_name,
          songsAdded: artist.song_count,
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
      <div style={{ color: "white" }}>
        <h3>Artist Placement According to Number of Songs Released </h3>
      </div>
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
