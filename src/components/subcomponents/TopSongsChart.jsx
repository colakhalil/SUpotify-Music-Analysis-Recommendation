import React from "react";
import PropTypes from "prop-types";

const TopSongsChart = ({ topSongs }) => {
  return (
    <div className="top-songs-chart">
      <h3 className="chart-title">Top Songs</h3>
      <ul className="top-songs-list">
        {topSongs.map((song, index) => (
          <li key={index} className="song-item">
            <span className="song-rank">#{index + 1}</span>
            <span className="song-title">{song.title}</span>
            <span className="song-plays">Plays: {song.plays}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

TopSongsChart.propTypes = {
  topSongs: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string.isRequired,
      plays: PropTypes.number.isRequired,
    })
  ).isRequired,
};

export default TopSongsChart;
