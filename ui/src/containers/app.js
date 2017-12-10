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
import IftttAddeditPage from './ifttt-addedit-page'
import ComponentsPage from  './components-page'


class App extends Component {
  render() {
    return (
      <div className="app">
        <Header {...this.props} />
        <div className="app-body">
          <Sidebar {...this.props} />
          <main className="main">
            <Container fluid>
              <Switch>
                <Route path="/main-page" name="MainPage" component={secure(MainPage)}/>
                <Route path="/actuators" name="ActuatorsPage" component={secure(ComponentsPage)}/>
                <Route path="/sensors" name="SensorsPage" component={secure(ComponentsPage)}/>
                <Route path="/ifttt-list" name="IftttPage" component={secure(IftttList)}/>
                <Route path="/ifttt-edit/:id" name="IftttAddeditPage" component={secure(IftttAddeditPage)}/>
                <Route path="/ifttt-add" name="IftttAddeditPage" component={secure(IftttAddeditPage)}/>
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