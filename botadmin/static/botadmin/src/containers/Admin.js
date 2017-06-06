import React from 'react';
import ManuscriptTable from "../components/ManuscriptTable";
import { connect } from "react-redux";
import { deleteManuscript, loadManuscripts } from "../actions/manuscripts";
import { getManuscriptApiUrl, getManuscriptsApiUrl } from "../utils/urls";
import * as toastr from "toastr";

const mapStateToProps = (state) => {
  return {
    manuscripts: state.manuscripts
  };
};

const mapDispatchToProps = (dispatch) => {
  dispatch(loadManuscripts());
  fetch(getManuscriptsApiUrl())
    .then(response => response.json())
    .then(manuscripts => dispatch(loadManuscripts(manuscripts)))
    .catch(error => dispatch(loadManuscripts(error)));
  return {
    deleteManuscript: (manuscriptId) => {
      if (window.confirm('Are you sure?')) {
        dispatch(deleteManuscript(manuscriptId));
        const timeoutHandleId = setTimeout(() => toastr.info('Trying to delete manuscript, please wait'), 300);
        fetch(getManuscriptApiUrl(manuscriptId), {
          method: 'DELETE'
        })
          .then(response => {
            clearTimeout(timeoutHandleId);
            dispatch(deleteManuscript(manuscriptId, response));
            toastr.success('Successfully deleted manuscript');
          })
          .catch(error => {
            dispatch(deleteManuscript(manuscriptId, error));
            toastr.error('Failed to delete manuscript');
          });
      }
    }
    // addManuscriptItem: () => {
    //   dispatch(addManuscriptItem(match.params.manuscriptId));
    // },
    // changeManuscriptProperty: (event, propertyName) => {
    //   dispatch(changeManuscriptProperty(match.params.manuscriptId, propertyName, event.target.value));
    // },
    // changeManuscriptItemProperty: (event, order, propertyName) => {
    //   dispatch(changeManuscriptItemProperty(match.params.manuscriptId, order, propertyName, event.target.value));
    // },
    // deleteManuscriptItem: (order) => {
    //   dispatch(deleteManuscriptItem(match.params.manuscriptId, order));
    // },
    // onSubmit: (event, manuscript) => {
    //   event.preventDefault();
    //   dispatch(editManuscript(manuscript));
    //   return sendManuscriptToApi(manuscript, 'PUT')
    //     .then(createdManuscript => dispatch(editManuscript(createdManuscript, createdManuscript)))
    //     .catch(error => dispatch(editManuscript(manuscript, error)));
    // }
  }
};

const Admin = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptTable);

export default Admin;
