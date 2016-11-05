import 'styles/mystyle.css';

import React from 'react';
import request from 'request';
import { Chart } from 'react-d3-core';
import { LineChart } from 'react-d3-basic';

class StationRecord extends React.Component {
  constructor() {
    super();
    this.state = {
      stationRecord: {name: '', line: [], price_history: []}
    };
    this.getStationRecord = this.getStationRecord.bind(this);
  }
  componentWillReceiveProps(nextProps) {
    this.getStationRecord(nextProps.stationId);
  }
  getStationRecord(stationId) {
    let that = this;
    let stationRecord = {};
    request(location.origin + '/wolsemap/station/' + stationId + '/', function(error, response, body) {
      if (!error && response.statusCode == 200) {
        stationRecord = JSON.parse(body);
      }
      that.setState({
        stationRecord: stationRecord
      });
    });
  }
  render() {
    let stationRecord = this.state.stationRecord;
    let title = stationRecord.name + ' ' + stationRecord.line;
    let data = stationRecord.price_history;
    let parseDate = d3.time.format('%Y-%m-%d').parse;

    let priceDomain = d3.extent(data, (d)=> {return d.price;});
    let depositDomain = d3.extent(data, (d)=> {return d.deposit;});
    priceDomain = [priceDomain[0] - 5, priceDomain[1] + 5];
    depositDomain = [depositDomain[0] - 100, depositDomain[1] + 100];
    return (
      <div>
        <div className="record">
          <LineChart
            title={title}
            data={data}
            width={800}
            height={300}
            margins={{top: 50, right: 100, bottom: 50, left: 100}}
            chartSeries={[
              {
                field: 'price',
                name: '월세',
                color: '#03C5F3',
                style: {
                  "strokeWidth": 5,
                  "strokeOpacity": 0.7,
                  "fillOpacity": 0.7
                }
              }
            ]}
            xDomain={d3.extent(data, (d)=> {return parseDate(d.date);})}
            yDomain={priceDomain}
            xScale='time'
            yLabel='가격(단위: 만)'
            xLabel='날짜'
            x={(d)=> {return parseDate(d.date);}}
          />
        </div>
        <div className="record">
          <LineChart
            title={title}
            data={data}
            width={800}
            height={300}
            margins={{top: 50, right: 100, bottom: 50, left: 100}}
            chartSeries={[
              {
                field: 'deposit',
                name: '보증금',
                color: '#029CDA',
                style: {
                  "strokeWidth": 5,
                  "strokeOpacity": 0.7,
                  "fillOpacity": 0.7
                }
              }
            ]}
            xDomain={d3.extent(data, (d)=> {return parseDate(d.date);})}
            yDomain={depositDomain}
            xScale='time'
            yLabel='가격(단위: 만)'
            xLabel='날짜'
            x={(d)=> {return parseDate(d.date);}}
          />
        </div>
      </div>
    );
  }
}

export default StationRecord;
