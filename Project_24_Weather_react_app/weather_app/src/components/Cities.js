import React from "react";

import City from "./City";

import "../styles/Cities.css";

function Cities(props){
    const cities = props.cities

    return (
        <div className="cities-group">
            {cities.map((city) => <City key={city} name={city} onClick={props.handleClick}/>)}
        </div>
    )
}

export default Cities;