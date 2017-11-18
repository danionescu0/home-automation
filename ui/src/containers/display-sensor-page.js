import React, {Component} from 'react';
import {Line} from 'react-chartjs-2';
import {CardColumns, Card, CardHeader, CardBody} from 'reactstrap';
import {getJson} from '../utils/fetch'

class DisplaySensorPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: null,
            lineGraph: lineGraph,
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
            var newDatasetTemplate = datasetTemplate;
            datasetTemplate.label = sensorId;
            datasetTemplate.data = data.map(datapoint => datapoint.value);
            var newLineGraph = lineGraph;
            lineGraph.datasets = [newDatasetTemplate];
            lineGraph.labels = data.map(datapoint => datapoint.date);
            this.setState({lineGraph: newLineGraph});
        });
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
                        <Line data={this.state.lineGraph} options={{maintainAspectRatio: false}} />
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
                        <Line data={this.state.lineGraph} options={{maintainAspectRatio: false}} />
                      </div>
                    </CardBody>
                  </Card>
                </CardColumns>
              </div>
            )
        }
}

const datasetTemplate = {
      label: 'My First dataset2',
      fill: false,
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
      data: ['1']
    };

const lineGraph = {
  labels: ['Loading data'],
  datasets: [datasetTemplate]
};


export default DisplaySensorPage;