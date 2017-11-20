import React, {Component} from 'react';
import RoomList from '../components/Widgets/RoomList'
import {getJson} from '../utils/fetch'
import {postJson} from "../utils/fetch";


class MainPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: null,
            room_data: [],
            periodicallyLoader: null
        }
    }

  componentDidMount() {
      this.loadData();
      this.state.periodicallyLoader = setInterval(this.loadData.bind(this), 7000);
  }

  componentWillUnmount() {
      clearInterval(this.state.periodicallyLoader);
  }

  actuatorHandler(id, value) {
       var postData = {
            'id' : id,
            'value': value
        };
        postJson(`/api/actuator`, postData).then(() => {
            console.log('changed');
        }, e => {
            console.log('error');
        });
  }

  loadData() {
        getJson(`/api/rooms`).then(data => {
            this.setState({room_data: data});
        })
  }

  render() {
    return (
      <div className="animated fadeIn">
          <RoomList room_data={this.state.room_data} actuatorHandler={this.actuatorHandler.bind(this)} />
      </div>
    )
  }
}

export default MainPage;