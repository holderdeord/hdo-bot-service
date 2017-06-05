import React from 'react';
import ManuscriptForm from "./ManuscriptForm";
import InfoManuscript from "../manuscripts/InfoManuscript";

export default class CreateManuscriptComponent extends React.Component {
  state = {
    manuscript: new InfoManuscript(),
    categories: []
  };

  // componentDidMount() {
  //   fetch('http://localhost:8000/api/categories/')
  //     .then(response => response.json())
  //     .then(categories => this.setState({ categories }));
  // }

  handleSubmit(event) {
    console.log('submitting', this.state.manuscript);
  }

  render() {
    return <ManuscriptForm manuscript={this.state.manuscript}
                           handleSubmit={event => this.handleSubmit(event)}/>;
  }
}
