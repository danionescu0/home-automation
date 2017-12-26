import React, {Component} from 'react';
import update from 'immutability-helper';
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
            console.log(data);
            this.setState({'configuration' : data});
        });
    }

    handleChange(arrayIndex, property, event) {
        let newValue = event.target.value;
        console.log(arrayIndex, property);
        let newConfiguration = this.state.configuration.map((element, index) => {
            if (index == arrayIndex) {
                return update(element,
                    {properties: {[property]: {$set: newValue}}}
                )
            }

            return Object.assign({}, element);
        });
        this.setState({configuration : newConfiguration});
    }


    handleSubmit(e) {
        e.preventDefault();
        postJson('/api/configuration', this.state.configuration, 'POST')
            .then(() => {
                console.log('success');
            }, e => {
                console.log('failed');
            });
    }

    render() {
        return (
            <Configuration configuration={this.state.configuration}
                          handleChange={this.handleChange.bind(this)}
                          handleSubmit={this.handleSubmit.bind(this)} />
        )
    }
}

export default withForm(withRouter(ConfigurationPage));