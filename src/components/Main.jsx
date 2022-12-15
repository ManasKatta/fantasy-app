import React, { useState } from "react";
import PlayerCard from "./PlayerCard";
import axios from "axios";
import { useEffect } from "react";
function Main() {
  const players = ["4046", "3198", "4034", "3321", "6794", "1466"];
  const trades = [["4046"], ["4984"]];
  const [trending, setTrending] = useState([]);

  useEffect(() => {
    axios
      .get("https://api.sleeper.app/v1/players/nfl/trending/add")
      .then((response) => {
        setTrending(response.data);
      });
  }, []);

  console.log(trending);
  return (
    <div className="flex flex-row justify-center justify-items-center bg-black h-screen py-20 px-10">
      <div className="flex flex-col text-white h-full font-bold bg-[#121212] rounded-lg py-2 px-2 overflow-auto scroll-smooth scrollbar-hide">
        Your Team
        {players.map((playerID) => (
          <PlayerCard playerID={playerID} />
        ))}
      </div>

      <div className="px-10"></div>

      <div className="text-white px-2 py-2 font-bold bg-[#121212] rounded-lg overflow-auto">
        Trade Suggestion
        {trades[0].map((playerID) => (
          <PlayerCard playerID={playerID} />
        ))}
        FOR
        {trades[1].map((playerID) => (
          <PlayerCard playerID={playerID} />
        ))}
      </div>
            
      {/* <div className="px-10"></div>

      <div className="flex flex-col text-white h-full font-bold bg-[#121212] rounded-lg py-2 px-2 overflow-auto scroll-smooth scrollbar-hide">
        Trending Players
        {trending.map((player) => (
          <PlayerCard playerID={player.player_id} />
        ))}
      </div> */}
    </div>
  );
}

export default Main;
