import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';


import IftttAddedit from '../components/Widgets/IftttAddedit'
import withForm from '../utils/form';
import {getJson} from '../utils/fetch'
import {postJson} from "../utils/fetch";


class IftttAddeditPage extends Component {
    constructor(props) {
      super(props);
      this.state = {
          'actuators' : [],
          'rule' : {
              'name' : 'Loading',
              'text': 'Loading',
              'active': true,
              'actuator_state': '',
              'actuator_id': '',
              'voice_text': ''
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
        getJson(`/api/actuators`).then(data => {
            this.setState({'actuators' : data});
        });
    }

    handleChange(field, event) {
        var value = event.target.value;
        if (['true', 'false'].indexOf(value) != -1) {
            value = {'true': true, 'false': false}[value];
        }
        var rule = {...this.state.rule};
        rule[field] = value;
        console.log(field, value);
        this.setState({rule});
    }

    handleSubmit(e) {
        e.preventDefault();
        console.log(this.state.rule);
        const ruleId = this.props.match.params.id;
        postJson(`/api/ifttt/${ruleId}`, this.state.rule).then(() => {
            console.log('success');
        }, e => {
            console.log('failde');
        });
    }

    render() {
        return (
            <IftttAddedit rule={this.state.rule} actuators={this.state.actuators}
                          handleChange={this.handleChange.bind(this)}
                          handleSubmit={this.handleSubmit.bind(this)} />
        )
    }
}

export default withForm(withRouter(IftttAddeditPage));