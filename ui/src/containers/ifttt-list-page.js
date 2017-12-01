import React, {Component} from 'react';

import IftttList from '../components/Widgets/IftttList'
import {getJson} from '../utils/fetch'
import {remove} from '../utils/fetch'


class IftttListPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: null,
            rules: [],
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

    deleteRule(id, e) {
        e.preventDefault();
        remove(`/api/ifttt/${id}`)
            .then(() => {
                this.loadData();
            }, e => {
                console.log('failed to delete');
            });
    };
    render() {
        return (
          <div className="animated fadeIn">
              <IftttList rules_data={this.state.rules} delete_rule={this.deleteRule.bind(this)} />
          </div>
        )
    }
}

export default IftttListPage;