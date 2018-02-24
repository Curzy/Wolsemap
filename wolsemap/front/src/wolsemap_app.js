import 'styles/wolsemap.scss';
import 'react-select/dist/react-select.css';

import React from 'react';
import ReactDOM from 'react-dom';
import request from 'request';

import Select from 'react-select';
import Title from './components/Title';
import StationRecord from './components/StationRecord';
import Wolsemap from './components/Wolsemap';

class WolsemapApp extends React.Component {
  constructor() {
    super();
    this.state = {
      stationList: [],
      selectedStation: {value: 441, label: '신림역 2호선'},
    };
    this.selectStation = this.selectStation.bind(this);
  }

  componentDidMount() {
    this.getStationList();
  }
  getStationList() {
    const that = this;
    let stationList = {};
    request.get(location.origin + '/wolsemap/stations/', function(error, response, body) {
      if (!error && response.statusCode == 200) {
        stationList = JSON.parse(body);
      }
      that.setState({
        stationList: stationList
      });
    });
  }
  render() {
    return (
        <div>
          <Title title='수도권 월세 노선도' description="매일밤 다방과 직방에서 새로운 정보를 가져옵니다"/>
          <div className="station-searchbar">
            <Select
              name="station-selector"
              value={this.state.selectedStation}
              options={this.state.stationList}
              onChange={this.selectStation}/>
          </div>
          <StationRecord stationId={this.state.selectedStation.value}/>
          <Wolsemap/>
          <div id="station-record"></div>
        </div>
    );
  }
  selectStation(val) {
    this.setState({
      selectedStation: val
    });
  }
}

ReactDOM.render(
    <WolsemapApp/>,
    document.getElementById('content')
);
