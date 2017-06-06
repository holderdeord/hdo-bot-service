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
  }
};

const Admin = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptTable);

export default Admin;
