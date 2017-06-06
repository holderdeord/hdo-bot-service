import React from 'react';
import ManuscriptForm from "../components/ManuscriptForm";
import { connect } from "react-redux";
import {
  addManuscript, addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty,
  deleteManuscriptItem, moveManuscriptItem, postManuscript
} from "../actions/manuscripts";
import { getManuscriptFromState, sendManuscriptToApi } from "../utils/manuscript";
import { getManuscriptsApiUrl } from "../utils/urls";

const mapStateToProps = (state) => {
  return {
    manuscript: getManuscriptFromState(state, -1)
  };
};

const mapDispatchToProps = (dispatch, {history}) => {
  dispatch(addManuscript());
  dispatch(addManuscriptItem(-1));
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem(-1));
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(-1, propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(-1, order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      dispatch(deleteManuscriptItem(-1, order));
    },
    moveManuscriptItemDown: (order) => {
      dispatch(moveManuscriptItem(-1, order, 1));
    },
    moveManuscriptItemUp: (order) => {
      dispatch(moveManuscriptItem(-1, order, -1));
    },
    onSubmit: (event, manuscript) => {
      event.preventDefault();
      dispatch(postManuscript(manuscript));
      return sendManuscriptToApi(manuscript, getManuscriptsApiUrl(), 'POST')
        .then(createdManuscript => {
          dispatch(postManuscript(manuscript, createdManuscript));
          history.push(`/edit/${createdManuscript.pk}`);
        })
        .catch(error => dispatch(postManuscript(manuscript, error)));
    }
  }
};

const CreateManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default CreateManuscript;
