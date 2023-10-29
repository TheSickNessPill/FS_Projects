import React from "react";

import "../styles/App.css";

import Header from "./Header";
import Body from "./Body";
import Separator from "./Separator";


function App(){
    return (
        <React.Fragment>
            <Header />
            <Separator />
            <Body />
            <Separator />
        </React.Fragment>
    );
}

export default App;