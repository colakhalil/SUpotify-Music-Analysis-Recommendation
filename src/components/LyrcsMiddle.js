import React, { useEffect, useState } from "react";
import "../pagesCSS/LyricsPage.css";

const formatLyrics = (lyrics) => {
  // Remove both "\n" and "\\n" newline characters
  return lyrics.replace(/\\n|\n/g, " ");
};

const LyrcsMiddle = ({ song }) => {
  const [lyrics, setLyrics] = useState("");

  useEffect(() => {
    const artistName = song.artists;
    const songName = song.title;

    /*artist name normalization and title normalization should be sone */
    const lyricsUrl = `http://127.0.0.1:8008/lyrics/${artistName}/${songName}`;

    fetch(lyricsUrl)
      .then((response) => response.text())
      .then((data) => {
        const decodedLyrics = data.replace(/\\u[\dA-F]{4}/gi, (match) =>
          String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16))
        );
        setLyrics(decodedLyrics);
      })
      .catch((error) => {
        console.error("Error fetching lyrics:", error);
      });
  }, [song]);

  return (
    <>
      <div className="lyrics-container">
        <div
          className="album-pic"
          style={{ backgroundImage: `url(${song.img})` }}
        ></div>
        <h1 className="song-name">{song.title}</h1>
        <h2 className="artist-name">{song.artist}</h2>
        <div className="lyrics">
          {lyrics ? formatLyrics(lyrics) : "Loading..."}
        </div>
      </div>
    </>
  );
};

export default LyrcsMiddle;
