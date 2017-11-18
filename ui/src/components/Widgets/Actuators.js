import React, {Component} from 'react';
import Slider from 'rc-slider';
import {
    Label,
    Input,
    Button
} from 'reactstrap';
import 'rc-slider/assets/index.css';


export const ACTUATOR_TYPE = {
    SWITCH: 'switch',
    PUSHBUTTON: 'pushbutton',
    DIMMER: 'dimmer'
};

const Actuators = ({actuators, actuatorHandler}) => {
    var executeInFuture;
    const pushButtonHandler = (event) => {
        actuatorHandler(event.target.id, true)
    };
    const switchHandler = (event) => {
        actuatorHandler(event.target.id, event.target.checked)
    };
    const sliderHandler = (actuatorId, value) => {
        clearTimeout(executeInFuture);
        executeInFuture = setTimeout(
          function () {
              actuatorHandler(actuatorId, value)
          }.bind(this),
          500
        );
    };

    return actuators.map((actuator, index) => {
        var actuatorHtml = "";
        if (actuator.type == ACTUATOR_TYPE.SWITCH) {
            var input = actuator.value == true ?
                (<Input id={actuator.id} type="checkbox" className="switch-input" onClick={switchHandler} defaultChecked/>) :
                (<Input id={actuator.id} type="checkbox" className="switch-input" onClick={switchHandler} />);
            actuatorHtml = (
                <Label className="switch switch-text switch-pill switch-primary">
                    {input}
                    <span className="switch-label" data-on="On" data-off="Off"></span>
                    <span className="switch-handle"></span>
                </Label>
            );
        } else if (actuator.type == ACTUATOR_TYPE.PUSHBUTTON) {
            actuatorHtml = (
                <Button  id={actuator.id}outline color="primary" size="sm" onClick={pushButtonHandler}>Activate</Button>
            )
        } else if (actuator.type == ACTUATOR_TYPE.DIMMER) {
            actuatorHtml = (
                <Slider id={actuator.id} min={0} max={255} defaultValue={actuator.value}
                        onChange={sliderHandler.bind(this, actuator.id)} />
            )
        }

        return (
                <tr key = {index}>
                    <td>{actuator.name}</td>
                    <td>
                        {actuatorHtml}
                    </td>
                </tr>
        )
    })
};


export default Actuators;