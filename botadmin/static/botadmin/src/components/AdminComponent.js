import React from 'react';
import ManuscriptTable from "./ManuscriptTable";

class AdminComponent extends React.Component {
  constructor() {
    super();
    this.state = { manuscripts: [] };
  }

  componentDidMount() {
    fetch('http://localhost:8000/api/manuscripts/')
      .then(response => response.json())
      .then(manuscripts => this.setState({ manuscripts }));
  }

  render() {
    return <ManuscriptTable manuscripts={this.state.manuscripts}/>;
  }
}

export default AdminComponent;
