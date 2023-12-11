import React, { useState } from "react";
import axios from "axios"; // Make sure axios is installed with `npm install axios`

const SearchBar = ({ setCurrentPlace, setSearchedArray }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    // Perform the search
    try {
      const response = await axios.get(
        `http://127.0.0.1:8008/search_user/${searchTerm}`
      );
      // Set the search results to the state
      console.log(response.data);
      setSearchedArray(response.data);
      // Change the current place to 'searched' to show the search results
      setCurrentPlace("searched");
    } catch (error) {
      console.error("Error fetching search results:", error);
      // You might want to handle errors, such as setting an error state or displaying a message
    }
  };

  return (
    <div className="search-bar-container">
      <form onSubmit={handleSearch} className="search-bar">
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={handleInputChange}
          className="search-input"
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>
    </div>
  );
};

export default SearchBar;
