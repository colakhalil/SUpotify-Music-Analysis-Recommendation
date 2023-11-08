import React from 'react';
import Rating from 'react-rating-stars-component';

const SongRating = ({ userRating, handleRatingChange }) => {
  return (
    <Rating
      count={5}
      value={userRating}
      size={24}
      activeColor="#ffd700"
      onChange={handleRatingChange}
    />
  );
};

export default SongRating;
