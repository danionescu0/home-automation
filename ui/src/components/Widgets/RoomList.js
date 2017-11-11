import React, {Component} from 'react';

import {
  Row,
  Col,
  Card,
  CardHeader,
  CardBody,
  Table,
} from 'reactstrap';

import Sensors from './Sensors'
import Actuators from './Actuators'

const RoomList = ({room_data, actuatorHandler}) => {
    var roomData = room_data.map((room, index) => {
        return (
            <Col key={index} xs="12" lg="6">
                <Card>
                    <CardHeader>
                        <i className="fa fa-align-justify"></i>
                        {room.name}
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <Sensors sensors={room.sensors} />
                    </CardHeader>
                    <CardBody>
                        <Table responsive striped>
                            <tbody>
                                <Actuators actuators={room.actuators} actuatorHandler={actuatorHandler} />
                            </tbody>
                        </Table>
                    </CardBody>
                </Card>
            </Col>
        )
    });

    return (
        <div className="animated fadeIn">
            <Row>
                {roomData}
            </Row>
        </div>
    )
};

export default RoomList;