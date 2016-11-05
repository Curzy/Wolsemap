import React from 'react';

class Wolsemap extends React.Component {
  render() {
    return (
        <div className="container">
          <object className="map" data="/static/svg/price_inserted_subway_linemap.svg" type="image/svg+xml" width="100%" id="subwaysvg"></object>
        </div>
    );
  }
}

export default Wolsemap;
