import React from 'react';
import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";
import {
  addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty, deleteManuscriptItem,
  editManuscript,
  loadManuscript, moveManuscriptItem
} from "../actions/manuscripts";
import { getManuscriptApiUrl } from "../utils/urls";
import { getManuscriptFromState, sendManuscriptToApi } from "../utils/manuscript";
import * as toastr from "toastr";

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
    moveManuscriptItemDown: (order) => {
      dispatch(moveManuscriptItem(match.params.manuscriptId, order, 1));
    },
    moveManuscriptItemUp: (order) => {
      dispatch(moveManuscriptItem(match.params.manuscriptId, order, -1));
    },
    onSubmit: (event, manuscript) => {
      event.preventDefault();
      dispatch(editManuscript(manuscript));
      const timeoutHandleId = setTimeout(() => toastr.info('Trying to save manuscript, Please wait'), 300);
      return sendManuscriptToApi(manuscript, getManuscriptApiUrl(manuscript.pk), 'PUT')
        .then(createdManuscript => {
          clearTimeout(timeoutHandleId);
          dispatch(editManuscript(createdManuscript, createdManuscript));
          toastr.success('Successfully saved manuscript')
        })
        .catch(error => {
          dispatch(editManuscript(manuscript, error));
          toastr.error('Failed to save manuscript');
        });
    }
  }
};

const EditManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default EditManuscript;
