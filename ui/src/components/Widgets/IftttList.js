import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import {withRouter} from 'react-router-dom'

import {
  Row,
  Col,
  Card,
  Badge,
  CardHeader,
  CardBody,
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Table,
} from 'reactstrap';


const IftttList = ({rules_data, show_delete_confirm, close_modal, modal_status, delete_rule}) => {
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
    const AddNewRule = withRouter(({ history }) => (
        <Button onClick={() => { history.push('/ifttt-add') }} size="sm" color="primary">
            <i className="fa fa-dot-circle-o"></i> Add new rule
        </Button>
    ));

    var iftttTable = rules_data.map((rule, index) => {
        return (
                <tr key = {index}>
                    <td>{rule.name}</td>
                    <td>{rule.text}</td>
                    <td>
                        <StatusBadge status={rule.active} />
                    </td>
                    <td>
                        <Link to="/" onClick={show_delete_confirm.bind(this, rule.id)}>Delete</Link>,
                        <Link to={"/ifttt-edit/" + rule.id}>Edit</Link>
                    </td>
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
                            <Modal isOpen={modal_status} className={'modal-warning'}>
                                  <ModalHeader>You are about to delete a rule</ModalHeader>
                                  <ModalBody>
                                        Confirm delete rule ?
                                  </ModalBody>
                                  <ModalFooter>
                                        <Button color="warning" onClick={delete_rule}>Delete</Button>{' '}
                                        <Button color="secondary" onClick={close_modal}>Cancel</Button>
                                  </ModalFooter>
                            </Modal>
                        </CardBody>
                        <AddNewRule/>
                    </Card>
                </Col>
            </Row>
        </div>
    )
};

export default IftttList;