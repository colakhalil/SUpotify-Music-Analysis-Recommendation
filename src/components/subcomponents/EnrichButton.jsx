import React, { useState } from 'react';

function EnrichButton({ genre, onEnrich }) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const enrichPlaylist = async () => {
    setIsLoading(true);
    setError('');
  
    try {
        const response = await fetch(`http://127.0.0.1:8008/enrich_rec/your_user_id/${genre}`);
        if (!response.ok) {
          // If the response is not OK, throw an error with the status
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Ensure that we're receiving a JSON response before trying to parse it
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new TypeError("Oops, we haven't got JSON!");
        }
        const data = await response.json(); // Directly parse the response body as JSON
        onEnrich(data);
      } catch (error) {
        console.error("Fetching error:", error);
        setError(`An error occurred: ${error.message}`);
      } finally {
        setIsLoading(false);
      }
      
  };
  

  return (
    <div>
      <button onClick={enrichPlaylist} disabled={isLoading}>
        {isLoading ? 'Enriching...' : 'Enrich Playlist'}
      </button>
      {error && <div>Error: {error}</div>}
    </div>
  );
}

export default EnrichButton;
