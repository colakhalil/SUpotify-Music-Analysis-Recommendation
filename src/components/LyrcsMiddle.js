const LyrcsMiddle = ({ song }) => {
  return (
    <>
      <div className="lyrics-container">
        <div
          className="album-cover"
          style={{ backgroundImage: `url(${song.img})` }}
        ></div>
        <h1 className="song-name">{song.title}</h1>
        <h2 className="artist-name">{song.artist}</h2>
        <div className="lyrics">
          {song.lyrics.map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
      </div>
    </>
  );
};

export default LyrcsMiddle;
