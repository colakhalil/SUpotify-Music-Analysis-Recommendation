import React, { useState, useEffect } from 'react';

const RecommendArtist = ({ currentUserId }) => {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    // Fetch artist recommendations using the provided API endpoint
    fetch(`http://127.0.0.1:8008/${currentUserId}/friend_artist_recommendations`)
      .then((response) => response.json())
      .then((data) => setRecommendations(data.recommendations))
      .catch((error) => console.error('Error fetching recommendations:', error));
  }, [currentUserId]);

  return (
    <div className="recommend-artist">
      <div className="artist-list">
        {recommendations.map((artist) => (
          <div key={artist.artist_id} className="artist-item">
            <img src={artist.picture} alt={artist.artist_name} />
            <h3 className="artist-name">{artist.artist_name}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendArtist;
