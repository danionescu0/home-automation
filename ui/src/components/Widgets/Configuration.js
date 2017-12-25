import React, {Component} from 'react';

import {
  Col,
  Button,
  Card,
  CardHeader,
  CardFooter,
  CardBody,
  Form,
  FormGroup,
  FormText,
  Label,
  Input,
} from 'reactstrap';


const Configuration = ({rule, handleChange, handleSubmit}) => {


    return (
      <div className="animated fadeIn">
          <Col xs="12" md="12">
            <Card>
              <CardHeader>
                <strong>Rule</strong>
              </CardHeader>

              <CardBody>
                <Form method="post" className="form-horizontal">
                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="text-input">Name</Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input type="text" id="text-input" name="text-input" placeholder="Name"
                             value="test"  />
                      <FormText color="muted">Rule name here, say something descriptive</FormText>
                    </Col>
                  </FormGroup>
                </Form>
              </CardBody>

              <CardFooter>
                <Button onClick={handleSubmit.bind(this)} type="submit" size="sm" color="primary">
                    <i className="fa fa-dot-circle-o"></i> Apply
                </Button>
              </CardFooter>
            </Card>
          </Col>
      </div>
    )
};

export default Configuration;