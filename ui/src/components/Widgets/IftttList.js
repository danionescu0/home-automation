import React, {Component} from 'react';

import {
  Row,
  Col,
  Card,
  Badge,
  CardHeader,
  CardBody,
  Table,
} from 'reactstrap';


const IftttList = ({rules_data}) => {

    const StatusBadge = ({status}) => {
        const statusBadgeToClass = {
            true : 'success',
            false : 'warning'
        };
        const statusText = {
            true: 'Active',
            false: 'Inactive'
        };
        return (
            <Badge color={statusBadgeToClass[status]}>{statusText[status]}</Badge>
        )
    };
    var iftttTable = rules_data.map((rule, index) => {
        return (
                <tr key = {index}>
                    <td>{rule.name}</td>
                    <td>{rule.text}</td>
                    <td>
                        <StatusBadge status={rule.active} />
                    </td>
                    <td>Delete, Edit</td>
                </tr>
        )
    });

    return (
        <div className="animated fadeIn">
            <Row>
                <Col>
                    <Card>
                        <CardHeader>
                            <i className="fa fa-align-justify"></i>
                            Rules:
                            &nbsp;&nbsp;&nbsp;&nbsp;
                        </CardHeader>
                        <CardBody>
                            <Table hover bordered striped responsive size="sm">
                                <thead>
                                    <tr>
                                        <th>Rule Name</th>
                                        <th>Content</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                        </tr>
                                </thead>
                                <tbody>
                                    {iftttTable}
                                </tbody>
                            </Table>
                        </CardBody>
                    </Card>
                </Col>
            </Row>
        </div>
    )
};

export default IftttList;