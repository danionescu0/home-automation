import React, {Component} from 'react';

import IftttList from '../components/Widgets/IftttList'
import {getJson} from '../utils/fetch'


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
        getJson(`/api/ifttt`).then(data => {
            this.setState({rules: data});
            console.log(data);
        });
  }

  render() {
    return (
      <div className="animated fadeIn">
          <IftttList rules_data={this.state.rules} />
      </div>
    )
  }
}

export default IftttListPage;