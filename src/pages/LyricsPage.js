import React from 'react';
import '../pagesCSS/LyricsPage.css';

// Dummy JSON data for the song, defined directly within this file
const LyricsSongInfo = {
  albumCover: "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/artistic-album-cover-design-template-d12ef0296af80b58363dc0deef077ecc_screen.jpg?ts=1696331695",// Replace with the actual image path
  songName: "Demir Attım Yalnızlığa",
  artistName: "Ebru Gündeş",
  lyrics: [
    "Sessiz bir köşede her şeyden uzak",
    "Meçhul yarınlara terk edilmişim",
    "Dostluklar yalanmış sevgiler tuzakmış",
    "Tuzak",
    "Hayret yanılmışım yalnızım şimdi",
    "Oysa mutluluğu hayal etmiştim",
    "Gidenler unutmuş aşkları yalanmış",
    "Yalan",
    "Güneşin doğuşu batışı farksız",
    "Nasıl yaşanırsa yaşadım ben aşksız",
    "Güneşin doğuşu batışı farksız",
    "Nasıl yaşanırsa yaşadım ben aşksız",
    "Demir attım yalnızlığa",
    "Bir hasret denizinde",
    "Ve şimdi hayallerim o günlerin izinde",
    "Yüreğimde duygular ümitlerim nerede",
    "Demir attım yalnızlığa",
    "Bir hasret denizinde",
    "Ve şimdi hayallerim o günlerin izinde",
    "Yüreğimde duygular ümitlerim nerede",
    "Şöyle bir düşünüp her şeyi birden",
    "Neden anıları bitirmeyişim",
    "Yalanmış sevgiler kalbimden uzakmış",
    "Uzak",
    "Boşa beklemişim yollara bakıp",
    "Kurak topraklara umutlar ekmişim",
    "Arzular avuttu gördüğüm hayalmiş",
    "Hayal",
    "Güneşin doğuşu batışı farksız",
    "Nasıl yaşanırsa yaşadım ben aşksız",
    "Güneşin doğuşu batışı farksız",
    "Nasıl yaşanırsa yaşadım ben aşksız",
    "Demir attım yalnızlığa",
    "Bir hasret denizinde",
    "Ve şimdi hayallerim o günlerin izinde",
    "Yüreğimde duygular ümitlerim nerede",
    "Demir attım yalnızlığa",
    "Bir hasret denizinde",
    "Ve şimdi hayallerim o günlerin izinde",
    "Yüreğimde duygular ümitlerim nerede",

    // ... More lyrics lines
  ]
};

const LyricsPage = () => {
  return (
    <div className="lyrics-container">
      <div className="album-cover" style={{ backgroundImage: `url(${LyricsSongInfo.albumCover})` }}></div>
      <h1 className="song-name">{LyricsSongInfo.songName}</h1>
      <h2 className="artist-name">{LyricsSongInfo.artistName}</h2>
      <div className="lyrics">
        {LyricsSongInfo.lyrics.map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
    </div>
  );
};

export default LyricsPage;
