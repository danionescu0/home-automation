import React, {Component} from 'react';
import {getJson} from '../utils/fetch'
import RoomList from '../components/Widgets/RoomList'


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

  loadData() {
        getJson(`/api/rooms`).then(data => {
            this.setState({room_data: data});
        });
  }

  render() {
    return (
      <div className="animated fadeIn">
          <RoomList room_data={this.state.room_data} />
      </div>
    )
  }
}

export default MainPage;