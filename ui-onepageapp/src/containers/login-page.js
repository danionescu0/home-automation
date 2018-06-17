import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';

import {
    Container, Row, Col, Alert, CardFooter, CardGroup, Card, CardBody, Button, Input, InputGroup, InputGroupAddon
} from 'reactstrap';

import withForm from '../utils/form';
import {performLogin} from "../utils/login";

class LoginPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            failedLogin: false
        }
    }

    handleSubmit(e) {
        const {form, history} = this.props;
        const successLoginHandler = () => {
            history.push('/');
            this.setState({failedLogin: true})
        };
        const failedLoginHandler = () => this.setState({failedLogin: true});
        performLogin(form.username, form.password).then(successLoginHandler.bind(this), failedLoginHandler.bind(this));
        e.preventDefault();
    }

    render() {
    const {handleInputChange} = this.props;

    return (
          <div className="app flex-row align-items-center">
            <Container>
              <Row className="justify-content-center">
                <Col md="8">
                  <CardGroup>
                    <Card className="p-4">
                      <CardBody>
                        <form onSubmit={this.handleSubmit.bind(this)}>
                            <h1>Login</h1>
                            <p className="text-muted">Login to Home Automation</p>
                            <InputGroup className="mb-3">
                              <InputGroupAddon><i className="icon-user"></i></InputGroupAddon>
                              <Input type="text" name="username" placeholder="Username" onChange={handleInputChange} />
                            </InputGroup>
                            <InputGroup className="mb-4">
                              <InputGroupAddon><i className="icon-lock"></i></InputGroupAddon>
                              <Input type="password" name="password" placeholder="Password" onChange={handleInputChange} />
                            </InputGroup>
                            <Row>
                              <Col xs="6">
                                <Button color="primary" className="px-4">Login</Button>
                              </Col>
                            </Row>
                        </form>
                      </CardBody>
                        {this.state.failedLogin && <CardFooter>
                                <Alert color="danger">Wrong username or password</Alert>
                            </CardFooter>
                        }
                    </Card>
                  </CardGroup>
                </Col>
              </Row>
            </Container>
          </div>
        );
    }
}

export default withForm(withRouter(LoginPage));