import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';


import {getJson} from '../utils/fetch'
import {postJson} from "../utils/fetch";

import {
  Col,
  Button,
  Card,
  CardHeader,
  CardFooter,
  CardBody,
  Form,
  FormGroup,
  Label,
  Input,
} from 'reactstrap';


class ActuatorsPage extends Component {
    constructor(props) {
          super(props);
          this.state = {
              'actuators' : [],
          };
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        getJson(`/api/actuators`).then(data => {
            this.setState({'actuators' : JSON.stringify(data, null, 4)});
        });
    }

    handleChange(event) {
        var value = event.target.value;
        this.setState({actuators: value});
    }

    handleSubmit(e) {
        e.preventDefault();
        postJson('/api/actuators', {'actuators': this.state.actuators})
            .then(() => {
                console.log('success');
            }, e => {
                console.log('failed');
            });
    }

    render() {
        return (
              <div className="animated fadeIn">
                  <Col xs="12" md="12">
                    <Card>
                      <CardHeader>
                        <strong>Actuators</strong>
                      </CardHeader>

                      <CardBody>
                        <Form method="post" className="form-horizontal">
                          <FormGroup row>
                            <Col md="3">
                              <Label htmlFor="textarea-input">Actuators</Label>
                            </Col>
                            <Col xs="12" md="9">
                              <Input type="textarea" name="textarea-input" id="textarea-input" rows="30"
                                     placeholder="Rule body" value={this.state.actuators}
                                     onChange={this.handleChange.bind(this)}  />
                            </Col>
                          </FormGroup>

                        </Form>
                      </CardBody>
                      <CardFooter>
                        <Button onClick={this.handleSubmit.bind(this)} type="submit" size="sm" color="primary">
                            <i className="fa fa-dot-circle-o"></i> Apply
                        </Button>
                      </CardFooter>
                    </Card>
                  </Col>
              </div>
            )
        }
}

export default withRouter(ActuatorsPage);