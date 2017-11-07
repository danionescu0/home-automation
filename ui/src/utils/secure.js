import React, {Component} from 'react';
import {withRouter} from 'react-router-dom'
import Auth from '../utils/auth';


export default function secure(ComposedComponent) {
    class Authentication extends Component {
        componentWillMount() {
            this.checkAuth();
        }

        componentWillUpdate() {
            this.checkAuth();
        }

       checkAuth() {
           const {history} = this.props;
           if (!Auth.isUserAuthenticated()) {
               history.push("/login");
           }
        }

        render() {
            return <ComposedComponent {...this.props} />
        }
    }


    return withRouter(Authentication);
}