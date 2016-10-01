import 'styles/mystyle.css';

import React from 'react';
import ReactDOM from 'react-dom';

class IndexPage extends React.Component {
  render() {
    return (
        <div>world!</div>
    );
  }
}

ReactDOM.render(
    <IndexPage/>,
    document.getElementById('content')
);

