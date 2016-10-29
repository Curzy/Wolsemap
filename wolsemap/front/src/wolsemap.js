import 'styles/mystyle.css';

import React from 'react';
import ReactDOM from 'react-dom';

class WolsemapPage extends React.Component {
  render() {
    return (
        <div>
          <Title title='수도권 월세 노선도' description="Cmd(Ctrl) + F로 원하는 역을 찾아보세요"/>
          <Wolsemap/>
        </div>
    )
  }
}

class Title extends React.Component {
  render () {
    return (
        <div className="title">
          <h1>{this.props.title}</h1>
          <p>{this.props.description}</p>
        </div>
    )
  }
}

class Wolsemap extends React.Component {
  render() {
    return (
        <div className="container">
          <object className="map" data="/static/svg/price_inserted_subway_linemap.svg" type="image/svg+xml" width="50%" id="subwaysvg"></object>
        </div>
    )
  }
}

ReactDOM.render(
    <WolsemapPage/>,
    document.getElementById('content')
);
