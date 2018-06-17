import React, {Component} from 'react';

import {
  Col,
  Row,
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


const Configuration = ({configuration, handleChange, handleSubmit}) => {
    let FormSeparator = ({name, index, enabled}) => {
        return (
            <FormGroup row>
                <Col md="3">
                    <b><Label htmlFor="text-input">{name}</Label></b>
                </Col>
                <Col md="3">
                  <Label check htmlFor="checkbox">
                      <Input type="checkbox" name="checkbox" checked={enabled}
                            onChange={handleChange.bind(this, index, "_enabled")}/> Enabled
                  </Label>
                </Col>
            </FormGroup>
        );
    };

    let formFields = configuration.map((config, index) => {
        let lastGroupName = '';

        return Object.keys(config['properties']).map((property, property_index) => {
            if (! (property in config['properties_description'])) {
                return;
            }
            let formGroupKey = index + "_" + property_index;
            let separator = false;
            if (lastGroupName != config['name']) {
                lastGroupName = config['name'];
                separator = true;
            }

            return (
                    <div key={formGroupKey}>
                        {separator ? (<FormSeparator name={config['name']} index={index}
                                                     enabled={config['properties']['_enabled']} />): null}
                        <FormGroup row>
                            <Col md="3">
                              <Label htmlFor="text-input">{property}</Label>
                            </Col>
                            <Col xs="12" md="9">
                              <Input type="text" id="text-input" name="text-input" placeholder="Name"
                                     value={config['properties'][property]}
                                     onChange={handleChange.bind(this, index, property)} />
                              <FormText color="muted">{config['properties_description'][property]}</FormText>
                            </Col>
                        </FormGroup>
                    </div>
                );
        });
    });

    return (
      <div className="animated fadeIn">
          <Col xs="12" md="12">
            <Card>
              <CardHeader>
                <strong>Configuration</strong>
              </CardHeader>

              <CardBody>
                <Form method="post" className="form-horizontal">
                    {formFields}
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