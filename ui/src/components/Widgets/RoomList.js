import React, {Component} from 'react';

import {
  Row,
  Col,
  Card,
  CardHeader,
  CardBody,
  Table,
} from 'reactstrap';

import {renderSensors} from './Sensors'
import Actuators from './Actuators'

const RoomList = ({room_data}) => {
    return (
        <div className="animated fadeIn">
            <Row>
                {doRenderRooms(room_data)}
            </Row>
        </div>
    )
};


const pushButtonClicked = (id)  => {
    console.log("button clicked:" + id);
};


const doRenderRooms = room_data => {
    return room_data.map((room, index) => {
        return (
            <Col key={index} xs="12" lg="6">
                <Card>
                    <CardHeader>
                        <i className="fa fa-align-justify"></i>
                        {room.name}
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        {renderSensors(room.sensors)}
                    </CardHeader>
                    <CardBody>
                        <Table responsive striped>
                            <tbody>
                                <Actuators actuators={room.actuators} pushButtonClicked={pushButtonClicked} />
                            </tbody>
                        </Table>
                    </CardBody>
                </Card>
            </Col>
        )
    })
};


export default RoomList;
