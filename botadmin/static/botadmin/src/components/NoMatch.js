import React from 'react';

class NoMatch extends React.Component {
  constructor(props) {
    super();
    this.pathName = props.location.pathname;
  }
  render() {
    return <div>No component available for <code>{this.pathName}</code></div>;
  }
}

export default NoMatch;
