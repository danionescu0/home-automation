import React, {Component} from 'react';
import {Switch, Route, Redirect} from 'react-router-dom';
import {Container} from 'reactstrap';
import Header from '../components/navigation/Header';
import Sidebar from '../components/navigation/Sidebar';
import Footer from '../components/navigation/Footer';
import Login from './login-page'
import secure from '../utils/secure'

import MainPage from './main-page';
import DisplaySensorPage from './display-sensor-page'
import IftttList from './ifttt-list-page'


class App extends Component {
  render() {
    return (
      <div className="app">
        <Header />
        <div className="app-body">
          <Sidebar {...this.props}/>

          <main className="main">
            <Container fluid>
              <Switch>
                <Route path="/main-page" name="MainPage" component={secure(MainPage)}/>
                <Route path="/ifttt-list" name="IftttPage" component={secure(IftttList)}/>
                <Route path="/display-sensor/:id" name="DisplaySensorPage" component={secure(DisplaySensorPage)}/>
                <Route path="/login" name="Login" component={Login}/>
                <Redirect from="/" to="/main-page"/>
              </Switch>
            </Container>
          </main>
        </div>
        <Footer />
      </div>
    );
  }
}

export default App;