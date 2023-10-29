import React from "react";
import axios from "axios";

import CurrentWeatherInfo from "./CurrentWeatherInfo";
import Separator from "./Separator";

import "../styles/WeatherInfo.css";

import config from "../../weather_app_config.json";


function WeatherInfo(props) {
    const [cityDiretionInfo, setCityDiretionInfo] = React.useState({});
    const [cityCurrentWeatherInfo, setCityCurrentWeatherInfo] = React.useState({});
    const [cityForecast5WeatherInfo, setCityForecast5WeatherInfo] = React.useState([]);

    React.useEffect(() => {
        if (props.cityName) {
            console.log(1);
            let coordinatesUrl = `http://api.openweathermap.org/geo/1.0/direct?q=${props.cityName}&limit=1&appid=${config.apiKey}`;
            axios.get(coordinatesUrl).then(result => {
                console.log("COORDS", result.data[0]);
                setCityDiretionInfo(result.data[0]);
            });
        }
        else {
            console.log(2);
        }
    }, [props]);

    React.useEffect(() => {
        if (cityDiretionInfo.lat && cityDiretionInfo.lon) {
            let currentWeatherInfoUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${cityDiretionInfo.lat}&lon=${cityDiretionInfo.lon}&units=metric&appid=${config.apiKey}`;
            axios.get(currentWeatherInfoUrl).then(result => {
                console.log("CURRENT_WEATHER", result.data);
                setCityCurrentWeatherInfo(result.data);
            });
        }
    }, [cityDiretionInfo, 1])

    React.useEffect(() => {
        if (cityDiretionInfo.lat && cityDiretionInfo.lon) {
            let currentWeatherInfoUrl = `https://api.openweathermap.org/data/2.5/forecast?lat=${cityDiretionInfo.lat}&lon=${cityDiretionInfo.lon}&units=metric&appid=${config.apiKey}`;
            axios.get(currentWeatherInfoUrl).then(result => {
                console.log("5DayForecast", result.data.list);
                setCityForecast5WeatherInfo(result.data.list);
            });
        }
    }, [cityDiretionInfo, 2]);

    return (
        <React.Fragment>
            <h1> CURRENT WEATHER </h1>
            <CurrentWeatherInfo
                key={cityCurrentWeatherInfo.dt}
                cityName={props.cityName}
                cityDiretionInfo={cityDiretionInfo}
                cityCurrentWeatherInfo={cityCurrentWeatherInfo}
            />
            <Separator />
            <div className="forecast-weather">
                <h1> FORECAST WEATHER </h1>
                {
                    cityForecast5WeatherInfo.map((period) =>
                        period.dt_txt.indexOf("09:00:00") >= 0 ?
                            <CurrentWeatherInfo
                                key={period.dt}
                                cityName={props.cityName}
                                cityDiretionInfo={cityDiretionInfo}
                                cityCurrentWeatherInfo={period}
                            />
                        :
                            undefined
                    )
                }
            </div>
        </React.Fragment>
    )
}

export default WeatherInfo;