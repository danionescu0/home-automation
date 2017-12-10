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
  FormText,
  Label,
  Input,
} from 'reactstrap';


class ComponentsPage extends Component {
    constructor(props) {
        super(props);
        this.paths = {'actuators' : '/api/actuators', 'sensors' : '/api/sensors'};
        this.pageName = {'actuators' : 'Actuators view', 'sensors' : 'Sensors view'};
        this.state = {
          'components' : [],
          'type' : 'actuators',
          'success' : null
        };
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        var type = this.props.location.pathname == '/actuators' ? 'actuators' : 'sensors';
        this.setState({'type': type}, function () {
            getJson(this.paths[this.state.type]).then(data => {
                this.setState({'components' : JSON.stringify(data, null, 4)});
            });
        });
    }

    handleChange(event) {
        var value = event.target.value;
        this.setState({components: value});
    }

    handleSubmit(e) {
        e.preventDefault();
        postJson(this.paths[this.state.type], {'components': this.state.components})
            .then(() => {
                this.setState({'success' : true});
            }, e => {
                this.setState({'success' : false});
            });
    }

    render() {
        var success = this.state.success ?
            (<FormText color="#FF0D45">Edit succesfull</FormText>) : (<FormText color="red">Edit failed</FormText> );
        return (
              <div className="animated fadeIn">
                  <Col xs="12" md="12">
                    <Card>
                      <CardHeader>
                        <strong>{this.pageName[this.state.type]}</strong>
                      </CardHeader>

                      <CardBody>
                        <Form method="post" className="form-horizontal">
                          <FormGroup row>
                            <Col xs="12" md="9">
                              <Input type="textarea" name="textarea-input" id="textarea-input" rows="30"
                                     placeholder="Rule body" value={this.state.components}
                                     onChange={this.handleChange.bind(this)}  />
                                {success}
                            </Col>
                          </FormGroup>
                        </Form>
                      </CardBody>
                      <CardFooter>
                        <Button onClick={this.handleSubmit.bind(this)} type="submit" size="sm" color="primary">
                            <i className="fa fa-dot-circle-o"></i> Apply changes
                        </Button>
                      </CardFooter>
                    </Card>
                  </Col>
              </div>
            )
        }
}

export default withRouter(ComponentsPage);