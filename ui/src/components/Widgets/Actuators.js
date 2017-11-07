import React, {Component} from 'react';

import {
    Label,
    Input,
    Button
} from 'reactstrap';
const ACTUATOR_TYPES = {
    SWITCH: 'switch',
    PUSHBUTTON: 'pushbutton',
    SLIDER: 'slider'
};


const Actuators = ({actuators, pushButtonClicked}) => {
    return actuators.map((actuator, index) => {
        var actuatorHtml = "";
        if (actuator.type == ACTUATOR_TYPES.SWITCH) {
            var input = actuator.value == true ?
                (<Input type="checkbox" className="switch-input" defaultChecked/>) :
                (<Input type="checkbox" className="switch-input" />);
            actuatorHtml = (
                <Label className="switch switch-text switch-pill switch-primary">
                    {input}
                    <span className="switch-label" data-on="On" data-off="Off"></span>
                    <span className="switch-handle"></span>
                </Label>
            );
        } else if (actuator.type == ACTUATOR_TYPES.PUSHBUTTON) {
            actuatorHtml = (
                <Button outline color="primary" size="sm" onClick={() => pushButtonClicked(actuator.id)}>Activate</Button>
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