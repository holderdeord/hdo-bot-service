import React from 'react';
import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";
import {
  addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty, deleteManuscriptItem, editManuscript,
  loadManuscript
} from "../actions/manuscripts";
import { getManuscriptApiUrl, getManuscriptsApiUrl } from "../utils/urls";
import { createManuscriptPayload } from "../utils/manuscript";

const mapStateToProps = (state, { match }) => {
  const manuscript = state.manuscripts.find(manuscript => manuscript.id === match.params.manuscriptId) || {
      name: '',
      type: 'info',
      items: []
    };
  return {
    manuscript
  };
};

const mapDispatchToProps = (dispatch, { match }) => {
  // let manuscript = addManuscript();
  // dispatch(manuscript);
  // dispatch(addManuscriptItem(manuscript.id));
  dispatch(loadManuscript(match.params.manuscriptId));
  fetch(getManuscriptApiUrl(match.params.manuscriptId))
    .then(response => response.json())
    .then(manuscript => dispatch(loadManuscript(match.params.manuscriptId, manuscript)));
  // .catch(error => dispatch(loadManuscript()))
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem(match.params.manuscriptId));
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(match.params.manuscriptId, propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(match.params.manuscriptId, order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      dispatch(deleteManuscriptItem(match.params.manuscriptId, order));
    },
    onSubmit: (event, manuscript) => {
      event.preventDefault();
      dispatch(editManuscript(manuscript));
      return fetch(getManuscriptsApiUrl(), {
        method: 'PUT',
        body: JSON.stringify(createManuscriptPayload(manuscript)),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
      })
        .then(response => response.json())
        .then(createdManuscript => dispatch(editManuscript(createdManuscript)))
        .catch(response => dispatch(editManuscript(manuscript, response)));
    }
  }
};

const EditManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default EditManuscript;


// import ManuscriptForm from "./ManuscriptForm";
// import InfoManuscript from "../manuscripts/InfoManuscript";
// import ManuscriptFactory from "../manuscripts/ManuscriptFactory";
//
// export default class EditManuscriptComponent extends React.Component {
//   state = {
//     manuscript: new InfoManuscript()
//   };
//
//   constructor(props) {
//     super(props);
//     this.manuscriptId = props.match.params.manuscriptId;
//     this.manuscriptFactory = new ManuscriptFactory();
//   }
//
//   componentDidMount() {
//     fetch(`http://localhost:8000/api/manuscripts/${this.manuscriptId}`)
//       .then(response => response.json())
//       .then(manuscriptData => this.setState({
//         manuscript: this.manuscriptFactory.loadManuscript(manuscriptData)
//       }));
//   }
//
//   handleSubmit(event) {
//     console.log('submitting', this.state.manuscript);
//   }
//
//   render() {
//     console.log('EditManuscriptComponent.render', this.state.manuscript);
//     return <ManuscriptForm manuscript={this.state.manuscript}
//                            handleSubmit={event => this.handleSubmit(event)}/>;
//   }
// }
