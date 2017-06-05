import React from 'react';
import ManuscriptForm from "./ManuscriptForm";

class ManuscriptCreateComponent extends React.Component {
  state = {
    categories: []
  };

  componentDidMount() {
    fetch('http://localhost:8000/api/categories/')
      .then(response => response.json())
      .then(categories => this.setState({ categories }));
  }

  render() {
    return <ManuscriptForm categories={this.state.categories} />;
  }
}

export default ManuscriptCreateComponent;
