import React from 'react';
import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";
import {
  addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty, deleteManuscriptItem,
  editManuscript,
  loadManuscript
} from "../actions/manuscripts";
import { getManuscriptApiUrl } from "../utils/urls";
import { getManuscriptFromState, sendManuscriptToApi } from "../utils/manuscript";

const mapStateToProps = (state, { match }) => {
  return {
    manuscript: getManuscriptFromState(state, match.params.manuscriptId)
  };
};

const mapDispatchToProps = (dispatch, { match }) => {
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
      return sendManuscriptToApi(manuscript, getManuscriptApiUrl(manuscript.id), 'PUT')
        .then(createdManuscript => dispatch(editManuscript(createdManuscript, createdManuscript)))
        .catch(error => dispatch(editManuscript(manuscript, error)));
    }
  }
};

const EditManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default EditManuscript;
