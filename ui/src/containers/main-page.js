import React, {Component} from 'react';
import {getJson} from '../utils/fetch'
import RoomList from '../components/Widgets/RoomList'
import {postJson} from "../utils/fetch";


class MainPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: null,
            room_data: [],
        }
    }

  componentDidMount() {
      this.loadData();
  }

  pushButtonClicked(e) {
   console.log("button clicked:", e, e.target.id, e.target.checked);
   var form = {
        'id' : e.target.id,
        'value': e.target.checked
    };
    console.log(form);

    postJson(`/api/actuator`, form).then(() => {
        console.log('changed');
    }, e => {
        console.log('error');
    });
  }

  loadData() {
        getJson(`/api/rooms`).then(data => {
            this.setState({room_data: data});
        });
  }

  render() {
    return (
      <div className="animated fadeIn">
          <RoomList room_data={this.state.room_data} pushButtonClicked={this.pushButtonClicked.bind(this)} />
      </div>
    )
  }
}

export default MainPage;