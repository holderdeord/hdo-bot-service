import React from 'react';
import ManuscriptForm from "./ManuscriptForm";
import InfoManuscript from "../manuscripts/InfoManuscript";
import ManuscriptFactory from "../manuscripts/ManuscriptFactory";

export default class EditManuscriptComponent extends React.Component {
  state = {
    manuscript: new InfoManuscript()
  };

  constructor(props) {
    super(props);
    this.manuscriptId = props.match.params.manuscriptId;
    this.manuscriptFactory = new ManuscriptFactory();
  }

  componentDidMount() {
    fetch(`http://localhost:8000/api/manuscripts/${this.manuscriptId}`)
      .then(response => response.json())
      .then(manuscriptData => this.setState({
        manuscript: this.manuscriptFactory.loadManuscript(manuscriptData)
      }));
  }

  handleSubmit(event) {
    console.log('submitting', this.state.manuscript);
  }

  render() {
    console.log('EditManuscriptComponent.render', this.state.manuscript);
    return <ManuscriptForm manuscript={this.state.manuscript}
                           handleSubmit={event => this.handleSubmit(event)}/>;
  }
}
