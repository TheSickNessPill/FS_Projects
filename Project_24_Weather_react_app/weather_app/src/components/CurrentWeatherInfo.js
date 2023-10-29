import React from "react";

import "../styles/currentWeatherInfo.css";

function getDateString(timeStamp){
    let date = new Date(timeStamp * 1000);
    let year = date.getFullYear();
    let month = ("0" + (date.getMonth() + 1)).slice(-2);
    let day = ("0" + date.getDate()).slice(-2);
    let hours = ("0" + date.getHours()).slice(-2);
    let minutes = ("0" + date.getMinutes()).slice(-2);
    let seconds = ("0" + date.getSeconds()).slice(-2);
    return `${year}.${month}.${day} ${hours}-${minutes}-${seconds}`;
}

function CurrentWeatherInfo(props) {

    return (
        <React.Fragment>
            <div className="weather-info-header">
                <h3>
                    Weather of {props.cityName} {props.cityCurrentWeatherInfo.dt ?
                            getDateString(props.cityCurrentWeatherInfo.dt) : undefined}
                </h3>
                {/* {props.cityDiretionInfo.lat ?
                    "[" : undefined}{props.cityDiretionInfo.lat} {props.cityDiretionInfo.lon}{props.cityDiretionInfo.lon ?
                        "]" : undefined} */}
            </div>
            <div className="weather-info-body">
                <div className="weather-clouds-info">
                    <p className="clouds-title"> Clouds: </p>
                    <p className="clouds-info">
                        {props.cityCurrentWeatherInfo.clouds ? `${props.cityCurrentWeatherInfo.clouds.all}%` : undefined}
                        {props.cityCurrentWeatherInfo.weather ? ` | ${props.cityCurrentWeatherInfo.weather[0].description}` : undefined}
                    </p>
                </div>
                <div className="weather-wind-info">
                    <p className="wind-title"> Wind: </p>
                    <p className="wind-info">
                        {props.cityCurrentWeatherInfo.wind ?
                            ` ${props.cityCurrentWeatherInfo.wind.deg}° | ${props.cityCurrentWeatherInfo.wind.speed} [m/h]` : undefined}
                    </p>
                </div>
                <div className="weather-temperature-info">
                    {props.cityCurrentWeatherInfo.main ? (
                        <table className="temperature-table">
                            <thead>
                                <tr>
                                    <th><p className="temperature-title"> Temperature: </p></th>
                                    <th>Now</th>
                                    <th>feels like</th>
                                    <th>Min</th>
                                    <th>Max</th>
                                    <th>Humidity</th>
                                    <th>Pressure</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td></td>
                                    <td> {`${props.cityCurrentWeatherInfo.main.temp}°`}</td>
                                    <td> {`${props.cityCurrentWeatherInfo.main.feels_like}°`}</td>
                                    <td> {`${props.cityCurrentWeatherInfo.main.temp_min}°`}</td>
                                    <td> {`${props.cityCurrentWeatherInfo.main.temp_max}°`}</td>
                                    <td> {`${props.cityCurrentWeatherInfo.main.humidity}%`}</td>
                                    <td> {`${props.cityCurrentWeatherInfo.main.pressure} [hPa]`}</td>
                                </tr>
                            </tbody>
                        </table>
                    ) : undefined}
                </div>
            </div>
        </React.Fragment>
    )
}

export default CurrentWeatherInfo;