import React from 'react';
import ManuscriptTable from "../components/ManuscriptTable";

class Admin extends React.Component {
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

export default Admin;
