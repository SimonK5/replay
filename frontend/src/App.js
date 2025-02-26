import "./App.css";
import React, { useState, useEffect } from "react";
import Form from "./Form";
import { DataVisual } from "./DataVisual";
import { Header } from "./Header";
import { Dots } from "loading-animations-react";

function App() {
  const [data, setData] = useState([{}]);
  const [showData, setShowData] = useState(false);

  function onSubmit(files) {
    setData([{}]);
    setShowData(true);

    if (files.length === 0) return;
    fetch("https://rivals-replay-stats.herokuapp.com/poststats", {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ replays: files }),
    })
      .then((response) => response.json())
      .then((stats) => {
        console.log("Success:", stats);
        setData(stats);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  useEffect(() => {
    document.title = "Rivals Replay Stats";
  }, []);

  return (
    <div className="App">
      <title>Rivals Replay Stats</title>
      <Header />
      {!showData && (
        <h1 className="description">
          Analyze your Rivals of Aether replay folder{" "}
        </h1>
      )}
      <Form handleSubmit={onSubmit} />
      {!showData && <img src={require("./roa_logo.png")} />}
      {showData &&
        (typeof data.num_replays === "undefined" ? (
          <Dots dotColors={["#3d3f47"]} />
        ) : (
          <div>
            <h1>Your Replay Folder Stats</h1>
            <DataVisual replay_data={data} />
          </div>
        ))}
    </div>
  );
}

export default App;
