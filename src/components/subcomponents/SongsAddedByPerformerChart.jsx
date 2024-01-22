import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import globalVar from "../../global.js";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const SongsAddedByPerformerChart = ({ userName }) => {
  const [data, setData] = useState([]);
  const [chartType, setChartType] = useState('LineChart');
  const [chartColor, setChartColor] = useState('#e0f00b'); // Default color

  // Function to handle chart type change
  const handleChartTypeChange = (event) => {
    setChartType(event.target.value);
  };

  // Function to render chart based on chart type
  const renderChart = () => {
    switch (chartType) {
      case 'BarChart':
        return (
          <BarChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="performer" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="songsAdded" fill={chartColor} /> // Use the selected color
          </BarChart>
        );
      case 'PieChart':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={data} dataKey="songsAdded" nameKey="performer" outerRadius={100} label>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color || chartColor} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        );
      case 'LineChart':
        return (
          <LineChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="performer" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="averageRating"
              stroke={chartColor} // Use the selected color
              activeDot={{ r: 8 }}
            />
          </LineChart>
        );
      default:
        return null;
    }
  };

  useEffect(() => {
    // Fetch data from the provided URL
    fetch("http://127.0.0.1:8008/" + userName + "/artist_song_count")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((fetchedData) => {
        // Transform the fetched data into the desired format
        const transformed = fetchedData.map((artist) => ({
          performer: artist.artist_name,
          songsAdded: artist.song_count,
          color: artist.color, // Assuming there is a color property in your data
        }));

        // Set the transformed data in state
        setData(transformed);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }, [userName]); // Added userName as a dependency for useEffect

  return (
    <div className="chart-container">
       <h3 className="chart-title">Songs Added by Performer</h3>
      {/* Add a select dropdown to allow users to change the chart type */}
      <select
        className="chart-selector"
        onChange={(e) => setChartType(e.target.value)}
        value={chartType}
      >
        
        <option value="BarChart">Bar Chart</option>
        <option value="PieChart">Pie Chart</option>
        <option value="LineChart">Line Chart</option> {/* New chart type added */}
      </select>
      <input
          type="color"
          className="color-selector" // Add a class for potential styling
          value={chartColor}
          onChange={(e) => setChartColor(e.target.value)}
          title="Choose chart color"
        />
      {/* Render the chart based on the current chart type */}
      {renderChart()}
    </div>
  );
};

export default SongsAddedByPerformerChart;
