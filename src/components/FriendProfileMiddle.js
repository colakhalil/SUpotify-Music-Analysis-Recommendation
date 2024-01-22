import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserPart from './subcomponents/UserPart';
import MonthlyAverageRatingsChart from "./subcomponents/FriendMonthlyR";
import SongsAddedByPerformerChart from "./subcomponents/FriendSongsAddedChart";
import FavoriteSongs90s from './subcomponents/FavoriteSongs90s'
import FavoriteRecentSongs from './subcomponents/FavoriteRecentSongs';
import globalVar from '../global';

const FriendProfileMiddle = ({ friendName }) => {

  const [friendData, setFriendData] = useState(null);

  useEffect(() => {
    const fetchFriendData = async () => {
      try {
        // Assuming friendName is the user_id required by your API
        const response = await axios.get(`http://127.0.0.1:8008/user_data_username/${friendName}`);
        setFriendData(response.data);
      } catch (error) {
        console.error('Error fetching friend data:', error);
      }
    };

    fetchFriendData();
  }, [friendName]);

  
  return (

    
    <div className="main-container">
      <div className="content-container">
        <UserPart userData={friendData} />
        <div className="friendship-button-container">
        </div>
         <FavoriteSongs90s  userName = {friendName}/>
          <FavoriteRecentSongs  userName = {friendName}/>
          <div style={{ display: "flex" }}>
          <div className="chart-wrapper">
            <MonthlyAverageRatingsChart userName={friendName} />
          </div>
          <div className="chart-wrapper">
            <SongsAddedByPerformerChart userName={friendName} />
          </div>
          </div>
      </div>
    </div>
    
  );
};

export default FriendProfileMiddle;
