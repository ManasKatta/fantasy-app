import React from "react";
import PlayerCard from "./PlayerCard";
import axios from "axios";
import { useEffect, useState } from "react";

function Main() {
  const [players, setPlayers] = useState([]);
  const [trades2, setTrades] = useState([]);
  //const players = ["4046", "3198", "4034", "2133", "7564", "3321", "6794", "1466", "5850"];
  const trades = [
    [
      ["4046", "6794"],
      ["4984", "4039"],
    ],
    [
      ["3198", "4034"],
      ["4984", "4039"],
    ],
  ];
  const [trending, setTrending] = useState([]);
  const [username, setUsername] = useState("");
  const [league, setLeague] = useState("");
  useEffect(() => {
    axios
      .get("https://api.sleeper.app/v1/players/nfl/trending/add")
      .then((response) => {
        setTrending(response.data);
      });
  }, []);

  const getTeam = (event) => {
    if (event.key === "Enter") {
      axios
        .get(`http://localhost:5000/getUserTeam/${username}/${league}`)
        .then((response) => {
          setPlayers(response.data);
        });
      axios.get(`http://localhost:7000/getTrades/`).then((response) => {
        setTrades(response.data);
      });
    }
  };

  // console.log(trending);
  return (
    <div>
      <form>
        <h3>username: </h3>
        <input
          type="text"
          name="username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          placeholder="Enter name here"
        ></input>
        <h3>league name:</h3>
        <input
          type="text"
          name="league"
          value={league}
          onChange={(event) => setLeague(event.target.value)}
          placeholder="Enter league name here"
          onKeyPress={getTeam}
        ></input>
      </form>
      <div className="flex flex-row justify-center justify-items-center bg-black h-screen py-20 px-10 overflow-auto scroll-smooth scrollbar-hide">
        <div className="flex flex-col text-white h-full font-bold bg-[#121212] rounded-lg py-2 px-2 overflow-auto scroll-smooth scrollbar-hide">
          Your Team
          {players.map((playerID) => (
            <PlayerCard playerID={playerID} key={playerID} />
          ))}
        </div>

        <div className="px-10"></div>
        {trades ? (
          <div className="text-white px-2 py-2 font-bold bg-[#121212] rounded-lg overflow-auto scroll-smooth scrollbar-hide">
            Trade Suggestion #1
            {trades[0][0].map((playerID) => (
              <PlayerCard playerID={playerID} />
            ))}
            FOR
            {trades[0][1].map((playerID) => (
              <PlayerCard playerID={playerID} />
            ))}
            Trade Suggestion #2
            {trades[1][0].map((playerID) => (
              <PlayerCard playerID={playerID} />
            ))}
            FOR
            {trades[1][1].map((playerID) => (
              <PlayerCard playerID={playerID} />
            ))}
          </div>
        ) : null}

        <div className="px-10"></div>

        {/*<div className="flex flex-col text-white h-full font-bold bg-[#121212] rounded-lg py-2 px-2 overflow-auto scroll-smooth scrollbar-hide">
          Trending Players
          {trending.map((player) => (
            <PlayerCard playerID={player.player_id} />
          ))}
          </div>*/}
      </div>
    </div>
  );
}

export default Main;
