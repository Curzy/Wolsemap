import React from 'react';

class Title extends React.Component {
  render () {
    return (
        <div className="title">
          <h1>{this.props.title}</h1>
          <p>{this.props.description}</p>
        </div>
    );
  }
}

export default Title;
