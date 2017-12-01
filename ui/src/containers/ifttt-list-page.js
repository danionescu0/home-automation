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
              delete_rule={this.deleteRule.bind(this)} />
          </div>
        )
    }
}

export default IftttListPage;