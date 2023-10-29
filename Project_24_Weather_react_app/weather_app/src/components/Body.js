import React from "react";
import axios from "axios";

import Separator from "./Separator";
import Cities from "./Cities";
import WeatherInfo from "./WeatherInfo";

import "../styles/Body.css";


function Body() {
    const cities = [
        "Los Angeles",
        "New York",
        "London",
        "Berlin",
        "Kyiv",
        "Moscow",
        "Tokyo"
    ]
    const [currentCity, setCurrentCity] = React.useState("");

    const handleClick = (name) => {
        setCurrentCity(name);
    }

    const resetCityInfo = () =>{
        setRequestCounter(0);
    }

    return (
        <React.Fragment>
            <Cities cities={cities} handleClick={handleClick}/>
            <Separator />
            <WeatherInfo cityName={currentCity}/>
        </React.Fragment>
    )
}

export default Body;