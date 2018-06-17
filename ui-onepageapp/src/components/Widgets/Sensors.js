import React, {Component} from 'react';
import {Link} from 'react-router-dom';


const SENSOR_TYPES_TO_IMAGE = {
    power: (<img src="../img/sensors/power.png" />),
    temperature: (<i className="fa fa-thermometer-full fa-lg mt-4"></i>),
    humidity: (<img src="../img/sensors/humidity.png" />),
    airPressure: (<img src="../img/sensors/airPressure.png" />),
    light: (<i className="fa fa-lightbulb-o fa-lg mt-4"></i>),
    voltage: (<i className="fa fa-battery-half fa-lg mt-4"></i>),
    rain: (<img src="../img/sensors/rain.png" />),
    presence: (<i className="fa fa-user-circle-o fa-lg mt-4"></i>),
    airPollution: (<img src="../img/sensors/airPollution.png" />),
    fingerprint: (<img src="../img/sensors/fingerprint.png" />),
    phone_is_home: (<img src="../img/sensors/phoneIsHome.png" />),
    flood: (<img src="../img/sensors/flood.png" />),
};


class Sensors extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return this.props.sensors.map((sensor, index) => {
            return (
                <span key = {index}>
                    <Link to={`/display-sensor/${sensor.id}`} title={sensor.name ? sensor.name : ''}>
                        {SENSOR_TYPES_TO_IMAGE[sensor.type]}
                    </Link>
                    {sensor.value}&nbsp;&nbsp;
                </span>

            )
        });
    }
}

export default Sensors;