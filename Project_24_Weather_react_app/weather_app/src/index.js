import React from "react";
import ReactDOM from "react-dom/client";

import App from "./components/App";

import "./styles/index.css"
import 'bootstrap/dist/css/bootstrap.min.css';


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);



// let coordinatesUrl = `http://api.openweathermap.org/geo/1.0/direct?q=${props.name}&limit=1&appid=${config.apiKey}`;

// if (selected != 1){
//     axios.get(coordinatesUrl).then(result => {
//         changeCoordinatesData(result.data[0]);
//         console.log("aaa", coordinatesData);
//     })
// }

// let currentWeatherUrl = (
//     `https://api.openweathermap.org/data/2.5/weather?lat=${coordinatesData.lat}&` +
//     `lon=${coordinatesData.lon}&appid=${config.apiKey}`
// );
// console.log(currentWeatherUrl);