import React from "react";


const Work = () => {
  const workInfoData = [
    {
      title: "Event Dates and Locations",
      text: "Discover where and when artists take the stage with us, and keep up with the rhythm of the music!",
    },
    {
      title: "Adding and Removing Friends",
      text: "Music is better when shared; discover new songs together and expand your musical world by sharing playlists and connecting with friends through our social music experience.",
    },
    {
      title: "Rate Album, Song, Artist",
      text: "Rate albums, songs, and artists individually to share your musical tastes and discover the community favorites.",
    },
    {
      title: "Add or Remove Song from Database",
      text: "Add your favorite tunes to our collection or remove a song from the database with ease.",
    },
    {
      title: "Recommended Playlists Based on Your Ratings",
      text: "Discover playlists curated just for you, tailored to your ratings for a personalized listening experience.",
    },
    {
      title: "Recommended Playlists Based on Genre",
      text: "Explore our recommended playlists, crafted to align with your favorite genres for a tailored musical journey.",
    },
    {
      title: "Recommended Playlists Based on Mood",
      text: "Immerse yourself in playlists recommended just for you, designed to match your mood and elevate your listening experience.",
    },
    {
      title: "Artist Reccomendation",
      text: "Uncover new favorites with our artist recommendations, expertly picked to resonate with your musical preferences.",
    },
    {
      title: "Export Songs",
      text: "Effortlessly export your top-rated songs and personally selected tracks right from our app to enjoy your music, anytime, anywhere.",
    },
    {
      title: "See Your Statistics",
      text: "View your music rating statistics and explore your friends' preferences to gain insights into your musical journey.",
    },
    {
      title: "Share Your Statistics on Social Media",
      text: "Share your music statistics on social media to showcase your unique taste and connect with fellow music enthusiasts.",
    },
    {
      title: "Change Your Friendship Type and See What Your Friends are Listening To",
      text: "Customize your friendships as private or public within the app, and if set to public, view your friends' latest listens and enjoy shared recommended playlists together.",
    },

  ];
  return (
    <div className="work-section-wrapper">
      <div className="work-section-top">
        <h1 className="primary-heading">How It Works</h1>
        <p className="primary-text">
          Explore the standout features that set our app apart with the cards below—your gateway to a unique and captivating musical voyage.
        </p>
      </div>
      <div className="work-section-bottom">
        {workInfoData.map((data) => (
          <div className="work-section-info" key={data.title}>

            <h2>{data.title}</h2>
            <p>{data.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Work;
