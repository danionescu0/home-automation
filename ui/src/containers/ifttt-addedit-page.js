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
              'edit' : true,
              'actuators' : [],
              'rule' : {
                  'name' : '',
                  'text': '',
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
        if (ruleId) {
            this.setState({edit : true});
            this.loadRuleData(ruleId);
        } else {
            this.setState({edit : false});
        }

        getJson(`/api/actuators`).then(data => {
            data.push({'id' : '', 'name': 'Select actuator'});
            this.setState({'actuators' : data});
        });
    }

    loadRuleData(ruleId) {
        getJson(`/api/ifttt-list`).then(data => {
            data.map((rule, index) => {
                if (rule.id == ruleId) {
                    this.setState({rule: rule});
                }
            });
        });
    }

    handleChange(field, event) {
        var value = event.target.value;
        if (['true', 'false'].indexOf(value) != -1) {
            value = {'true': true, 'false': false}[value];
        }
        var rule = {...this.state.rule};
        rule[field] = value;
        this.setState({rule});
    }

    handleSubmit(e) {
        e.preventDefault();
        const ruleId = this.props.match.params.id;
        var method = this.state.edit ? 'POST' : 'PUT';
        var url = this.state.edit ? `/api/ifttt/${ruleId}` : '/api/ifttt';
        postJson(url, this.state.rule, method)
            .then(() => {
                this.submitSuccess();
            }, e => {
                console.log('failed');
            });
    }

    submitSuccess() {
        this.props.history.push('/ifttt-list');
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