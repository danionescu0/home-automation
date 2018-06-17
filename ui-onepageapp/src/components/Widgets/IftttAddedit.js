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


const IftttAddedit = ({rule, actuators, handleChange, handleSubmit}) => {
    var actuatorSelect = actuators.map((actuator, index) => {
          return (
              <option key={index} value={actuator['id']}>
                  {actuator['room'] + ": " + actuator['name']}
              </option>
          );
        });

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
                             value={rule.name} onChange={handleChange.bind(this, 'name')} />
                      <FormText color="muted">Rule name here, say something descriptive</FormText>
                    </Col>
                  </FormGroup>
                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="textarea-input">Body</Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input type="textarea" name="textarea-input" id="textarea-input" rows="5"
                             placeholder="Rule body" value={rule.text} onChange={handleChange.bind(this, 'text')}  />
                      <FormText color="muted">Example: and  ( eq(A[livingCourtains], On), eq(TIME, 07:03))</FormText>
                    </Col>
                  </FormGroup>

                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="selectSm">Actuator name</Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input type="select" name="selectSm" id="SelectLm" size="sm" value={rule.actuator_id}
                          onChange={handleChange.bind(this, 'actuator_id')} >
                          {actuatorSelect}
                      </Input>
                    </Col>
                  </FormGroup>
                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="text-input">Actuator value</Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input type="text" name="text-input" placeholder="Actuator value"
                        value={rule.actuator_state} onChange={handleChange.bind(this, 'actuator_state')} />
                      <FormText color="muted">True, False or 1-255</FormText>
                    </Col>
                  </FormGroup>
                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="text-input">Text to speech</Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input type="text" id="text-input" name="text-input" placeholder="Text to speech"
                            value={rule.voice_text} onChange={handleChange.bind(this, 'voice_text')}  />
                      <FormText color="muted">
                          Some text, sensors and actuators placeholders are permitted, ex: S[humidity_outside], A[door]
                      </FormText>
                    </Col>
                  </FormGroup>
                  <FormGroup row>
                    <Col md="3">
                      <Label htmlFor="text-input">Email notification</Label>
                    </Col>
                    <Col xs="12" md="9">
                      <Input type="text" id="text-input" name="text-input" placeholder="Email notification"
                            value={rule.email_text} onChange={handleChange.bind(this, 'email_text')}  />
                      <FormText color="muted">
                          Some text, sensors and actuators placeholders are permitted, ex: S[humidity_outside], A[door]
                      </FormText>
                    </Col>
                  </FormGroup>
                  <FormGroup row>
                    <Col md="3">
                      <Label>Is rule active</Label>
                    </Col>
                    <Col md="9">
                      <FormGroup check>
                        <div className="radio">
                          <Label check htmlFor="radio1">
                            <Input type="radio" id="radio1" name="radios" value="true"
                                   checked={rule.active} onChange={handleChange.bind(this, 'active')}  /> Yes
                          </Label>
                        </div>
                        <div className="radio">
                          <Label check htmlFor="radio2">
                            <Input type="radio" id="radio2" name="radios" value="false"
                                   checked={!rule.active} onChange={handleChange.bind(this, 'active')}  /> No
                          </Label>
                        </div>
                      </FormGroup>
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

export default IftttAddedit;