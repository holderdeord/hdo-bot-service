import React from 'react';
import ManuscriptForm from "../components/ManuscriptForm";
import { connect } from "react-redux";
import {
  addManuscript, addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty,
  deleteManuscriptItem, postManuscript
} from "../actions/manuscripts";
import { getManuscriptFromState, sendManuscriptToApi } from "../utils/manuscript";
import { getManuscriptsApiUrl } from "../utils/urls";

const mapStateToProps = (state) => {
  return {
    manuscript: getManuscriptFromState(state, -1)
  };
};

const mapDispatchToProps = (dispatch, {history}) => {
  let manuscript = addManuscript();
  dispatch(manuscript);
  dispatch(addManuscriptItem(manuscript.id));
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem(manuscript.id));
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(manuscript.id, propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(manuscript.id, order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      dispatch(deleteManuscriptItem(manuscript.id, order));
    },
    onSubmit: (event, manuscript) => {
      event.preventDefault();
      dispatch(postManuscript(manuscript));
      return sendManuscriptToApi(manuscript, getManuscriptsApiUrl(), 'POST')
        .then(createdManuscript => {
          dispatch(postManuscript(manuscript, createdManuscript))
          history.push(`/edit/${createdManuscript.pk}`)
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
