import React, {Component} from 'react';
import {Line} from 'react-chartjs-2';
import {CardColumns, Card, CardHeader, CardBody} from 'reactstrap';
import {getJson} from '../utils/fetch'

class DisplaySensorPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: null,
            firstLineGraph: getDatasetTemplate("Loading...", [], []),
            secondLineGraph: getDatasetTemplate("Loading...", [], []),
            graphName: null
        }
    }

    componentDidMount() {
        this.loadSensorData();
    }

    loadSensorData() {
        const sensorId = this.props.match.params.id;
        this.setState({graphName:  this.props.match.params.id});
        getJson(`/api/sensor/${sensorId}`).then(data => {
            let lastDay = (Math.round(Date.now() / 1000)) - 3600 * 24;
            let last7Days = (Math.round(Date.now() / 1000)) - 3600 * 24 * 7;
            this.setState({firstLineGraph: this.getGraphDetails(sensorId, data, lastDay)});
            this.setState({secondLineGraph: this.getGraphDetails(sensorId, data, last7Days)});
        });
    }

    getGraphDetails(sensorId, data, fromTimestamp) {
        const filteredData = data.filter(row => row.timestamp > fromTimestamp);

        return getDatasetTemplate(sensorId,
            filteredData.map(datapoint => datapoint.value),
            filteredData.map(datapoint => datapoint.date));
    }

    render() {
        return (
              <div className="animated fadeIn">
                <CardColumns className="cols-2">
                  <Card>
                    <CardHeader>
                        {this.state.graphName} last day
                        <div className="card-actions">
                        </div>
                    </CardHeader>
                    <CardBody>
                      <div className="chart-wrapper">
                        <Line data={this.state.firstLineGraph} options={{maintainAspectRatio: false}} />
                      </div>
                    </CardBody>
                  </Card>
                  <Card>
                    <CardHeader>
                      {this.state.graphName} last 7 days
                      <div className="card-actions">
                      </div>
                    </CardHeader>
                    <CardBody>
                      <div className="chart-wrapper">
                        <Line data={this.state.secondLineGraph} options={{maintainAspectRatio: false}} />
                      </div>
                    </CardBody>
                  </Card>
                </CardColumns>
              </div>
            )
        }
}

function getDatasetTemplate(title, values, labels) {
    return {
      labels: labels,
      datasets: [{
          fill: false,
          label: title,
          lineTension: 0.1,
          backgroundColor: 'rgba(75,192,192,0.4)',
          borderColor: 'rgba(75,192,192,1)',
          borderCapStyle: 'butt',
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: 'miter',
          pointBorderColor: 'rgba(75,192,192,1)',
          pointBackgroundColor: '#fff',
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: 'rgba(75,192,192,1)',
          pointHoverBorderColor: 'rgba(220,220,220,1)',
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: values
        }]
    }
}


export default DisplaySensorPage;