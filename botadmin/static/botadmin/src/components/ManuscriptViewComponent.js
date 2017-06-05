import React from 'react';

class ManuscriptViewComponent extends React.Component {
  constructor(props) {
    super(props);
    this.manuscriptId = props.match.params.manuscriptId;
  }

  render() {
    return <div>test {this.manuscriptId}</div>;
  }
}

export default ManuscriptViewComponent;
