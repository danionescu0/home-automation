import React, {Component} from 'react';

const SENSOR_TYPES_TO_CLASS = {
    power: 'fa-battery-half',
    temperature: 'fa-thermometer-full',
    humidity: 'humidity',
    air_pressure: 'airPressure',
    light: 'fa-lightbulb-o',
    voltage: 'voltage',
    rain: 'rain',
    presence: 'fa-user-circle-o',
    air_pollution: 'airPollution',
    fingerprint: 'fingerprint',
    phone_is_home: 'phoneIsHome',
};


export const renderSensors = sensors => {
    return sensors.map((sensor, index) => {
        return (
            <span key = {index}>
                <i className={'fa ' + SENSOR_TYPES_TO_CLASS[sensor.type] +  ' fa-lg mt-4'}></i>
                {sensor.value}&nbsp;&nbsp;
            </span>
        )
    });
};