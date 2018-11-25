import React, {Component} from 'react';

import IftttList from '../components/Widgets/IftttList'
import {getJson} from '../utils/fetch'
import {postJson} from "../utils/fetch";
import {remove} from '../utils/fetch'
import update from 'immutability-helper';


class IftttListPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: null,
            rules: [],
            deleteModalOpen: false,
            deleteId : null
        }
    }

    componentDidMount() {
        this.loadData();
    }

    loadData() {
        getJson(`/api/ifttt-list`).then(data => {
            this.setState({rules: data});
        });
    }

    toggleRuleState(id, active, event) {
        event.preventDefault();
        let newRule = this.state.rules.filter(rule => rule.id === id)[0];
        newRule.active = !active;
        const newRules = this.state.rules.map((rule, index) => {
            return rule.id === id ? Object.assign({}, newRule) : Object.assign({}, rule);
        });
        this.setState({rules : newRules});
        postJson(`/api/ifttt/${id}`, newRule, 'POST')
            .then(() => {
                console.log('success');
            }, e => {
                console.log('failed');
            });
    }

    showDeleteConfirm(id, e) {
        e.preventDefault();
        this.setState({deleteModalOpen: true});
        this.setState({deleteId: id});
    };

    closeModal() {
        this.setState({deleteModalOpen: false});
    };

    deleteRule() {
        remove(`/api/ifttt/${this.state.deleteId}`)
            .then(() => {
                this.closeModal();
                this.loadData();
            }, e => {
                this.closeModal();
                console.log('failed to delete');
            });
    };

    render() {
        return (
          <div className="animated fadeIn">
              <IftttList rules_data={this.state.rules} show_delete_confirm={this.showDeleteConfirm.bind(this)}
              close_modal={this.closeModal.bind(this)} modal_status={this.state.deleteModalOpen}
              delete_rule={this.deleteRule.bind(this)} toggle_rule={this.toggleRuleState.bind(this)}/>
          </div>
        )
    }
}

export default IftttListPage;