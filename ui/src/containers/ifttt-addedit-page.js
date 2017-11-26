import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';

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

import withForm from '../utils/form';
import {getJson} from '../utils/fetch'
import {postJson} from "../utils/fetch";

class IftttAddeditPage extends Component {
    constructor(props) {
      super(props);
      this.state = {
          'rule' : {
              'name' : 'Loading',
              'text': 'Loading',
              'active': true
          }
      };
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        const ruleId = this.props.match.params.id;
        getJson(`/api/ifttt`).then(data => {
            data.map((rule, index) => {
                if (rule.id == ruleId) {
                    this.setState({rule: rule});
                }
            });
        });
    }

    handleChange(field, event) {
        var rule = {...this.state.rule}
        rule[field] = event.target.value;
        console.log(rule);
        this.setState({rule});
    }

    handleSubmit(e) {
        console.log('submit');
        const {form} = this.props;
        e.preventDefault();
        console.log(form);
        const ruleId = this.props.match.params.id;
        postJson(`/api/ifttt/${ruleId}`, this.state.rule).then(() => {
            console.log('success');
        }, e => {
            console.log('failde');
        });
    }

    render() {
        const {handleInputChange} = this.props;
        return (
          <div className="animated fadeIn">
              <Col xs="12" md="12">
                <Card>
                  <CardHeader>
                    <strong>Edit Rule</strong>
                  </CardHeader>

                  <CardBody>
                    <Form method="post" className="form-horizontal">
                      <FormGroup row>
                        <Col md="3">
                          <Label htmlFor="text-input">Name</Label>
                        </Col>
                        <Col xs="12" md="9">
                          <Input type="text" id="text-input" name="text-input" placeholder="Name"
                                 value={this.state.rule.name} onChange={this.handleChange.bind(this, 'name')} />
                          <FormText color="muted">Rule name here, say something descriptive</FormText>
                        </Col>
                      </FormGroup>
                      <FormGroup row>
                        <Col md="3">
                          <Label htmlFor="textarea-input">Body</Label>
                        </Col>
                        <Col xs="12" md="9">
                          <Input type="textarea" name="textarea-input" id="textarea-input" rows="5"
                                 placeholder="Rule body" value={this.state.rule.text} onChange={this.handleChange.bind(this, 'text')} />
                          <FormText color="muted">Example: and  ( eq(A[livingCourtains], On), eq(TIME, 07:03))</FormText>
                        </Col>
                      </FormGroup>

                      <FormGroup row>
                        <Col md="3">
                          <Label htmlFor="selectSm">Actuator name</Label>
                        </Col>
                        <Col xs="12" md="9">
                          <Input type="select" name="selectSm" id="SelectLm" size="sm">
                            <option value="0">Please select</option>
                            <option value="1">Option #1</option>
                            <option value="2">Option #2</option>
                            <option value="5">Option #5</option>
                          </Input>
                        </Col>
                      </FormGroup>
                      <FormGroup row>
                        <Col md="3">
                          <Label htmlFor="text-input">Actuator value</Label>
                        </Col>
                        <Col xs="12" md="9">
                          <Input type="text" id="text-input" name="text-input" placeholder="Some value"/>
                          <FormText color="muted">True, False or 1-255</FormText>
                        </Col>
                      </FormGroup>
                      <FormGroup row>
                        <Col md="3">
                          <Label htmlFor="text-input">Text to speech</Label>
                        </Col>
                        <Col xs="12" md="9">
                          <Input type="text" id="text-input" name="text-input" placeholder="Text to speech"/>
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
                                <Input type="radio" id="radio1" name="radios" value="option1"
                                       checked={this.state.rule.active} onChange={handleInputChange} /> Yes
                              </Label>
                            </div>
                            <div className="radio">
                              <Label check htmlFor="radio2">
                                <Input type="radio" id="radio2" name="radios" value="option2"
                                       checked={!this.state.rule.active} onChange={handleInputChange} /> No
                              </Label>
                            </div>
                          </FormGroup>
                        </Col>
                      </FormGroup>
                    </Form>
                  </CardBody>
                  <CardFooter>
                    <Button onClick={this.handleSubmit.bind(this)} type="submit" size="sm" color="primary">
                        <i className="fa fa-dot-circle-o"></i> Modify
                    </Button>
                  </CardFooter>
                </Card>
              </Col>
          </div>
        )
    }
}

export default withForm(withRouter(IftttAddeditPage));