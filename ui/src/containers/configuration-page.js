import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';


import Configuration from '../components/Widgets/Configuration'
import withForm from '../utils/form';
import {getJson} from '../utils/fetch'
import {postJson} from "../utils/fetch";


class ConfigurationPage extends Component {
    constructor(props) {
          super(props);
          this.state = {
              'configuration' : []
          };
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        getJson(`/api/configuration`).then(data => {
            data.push({'id' : '', 'name': 'Select actuator'});
            this.setState({'actuators' : data});
        });
    }

    handleChange(field, event) {
        var value = event.target.value;
        // var rule = {...this.state.rule};
        // rule[field] = value;
        // this.setState({rule});
    }

    handleSubmit(e) {
        e.preventDefault();
        // postJson(url, this.state.rule, method)
        //     .then(() => {
        //         this.submitSuccess();
        //     }, e => {
        //         console.log('failed');
        //     });
    }

    // submitSuccess() {
    //     this.props.history.push('/ifttt-list');
    // }

    render() {
        return (
            <Configuration configuration={this.state.configuration}
                          handleChange={this.handleChange.bind(this)}
                          handleSubmit={this.handleSubmit.bind(this)} />
        )
    }
}

export default withForm(withRouter(ConfigurationPage));