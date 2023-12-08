import React from "react";
import Rating from "react-rating-stars-component";

const SongRating = ({ userRating, onRatingChange }) => {
  return (
    <Rating
      onChange={onRatingChange}
      count={5}
      value={userRating}
      size={24}
      activeColor="#ffd700"
    />
  );
};

export default SongRating;
