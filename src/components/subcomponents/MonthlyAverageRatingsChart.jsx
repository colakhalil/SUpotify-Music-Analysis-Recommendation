import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

import globalVar from "../../global.js";

const MonthlyAverageRatingsChart = ({ userName }) => {
  const [data, setData] = useState([]);
  const [chartType, setChartType] = useState('LineChart');
  const [chartColor, setChartColor] = useState('#8884d8'); // Default color


  // Function to handle chart type change
  const handleChartTypeChange = (event) => {
    setChartType(event.target.value);
  };

  // Function to render chart based on chart type
  const renderChart = () => {
    switch (chartType) {
      case 'LineChart':
        return (
          <LineChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
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
      case 'BarChart':
        return (
          <BarChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="averageRating" fill={chartColor} />
          </BarChart>
        );
      case 'AreaChart':
        return (
          <AreaChart width={500} height={300} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="averageRating" stroke={chartColor} fill={chartColor} />
          </AreaChart>
        );
      default:
        return null;
    }
  };

  useEffect(() => {
    // Fetch data from the provided URL
    fetch("http://127.0.0.1:8008/" + userName + "/monthly_average_rating")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((fetchedData) => {
        // Extract the monthly average ratings from the response
        const monthlyRatings = fetchedData.monthly_average_ratings || [];

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
  }, [userName]); // Added userName as a dependency for useEffect

  return (
    <div className="chart-container">
    <h3 className="chart-title">Monthly Average Ratings</h3>
    <div className="chart-controls">
      <select
        className="chart-selector"
        onChange={(e) => setChartType(e.target.value)}
        value={chartType}
      >
        <option value="LineChart">Line Chart</option>
        <option value="BarChart">Bar Chart</option>
        <option value="AreaChart">Area Chart</option>
      </select>
      <input
        type="color"
        value={chartColor}
        onChange={(e) => setChartColor(e.target.value)}
        title="Choose your color"
      />
    </div>
    <ResponsiveContainer width="99%" height={300}>
      {renderChart()}
    </ResponsiveContainer>
  </div>






  );
};

export default MonthlyAverageRatingsChart;
