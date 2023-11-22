const Playlist = ({ name, thumbnail, onClick, additionalInfo }) => { // additionalInfo gibi ek bir prop eklendi
  return (
    <div className="Playlist" onClick={onClick}>
      <img src={thumbnail} alt={`${name} cover`} className="lastPlaylists-thumbnail" />
      <div className="lastPlaylists-name">{name}</div>
      {additionalInfo && <div className="playlist-additional-info">{additionalInfo}</div>} // Ek bilgiyi göster
    </div>
  );
};
export default Playlist;