import React from "react";
import { Button } from "react-bootstrap";

import "../styles/City.css";

function City(props){
    const [selected, changeSelected] = React.useState(0);

    const handleClick = () => {
        changeSelected(selected === 0 ? 1 : 0);
        props.onClick(props.name);
    }

    return (
        <Button choosen={selected} variant={(selected % 2) ? "success" : "warning"} onClick={handleClick}>
            {props.name}
        </Button>
    );
}

export default City;