import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";
import {
  addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty, deleteManuscriptItem,
  editManuscript, loadManuscript,
  moveManuscriptItem
} from "../actions/manuscripts";
import { getManuscriptApiUrl } from "../utils/urls";
import { getManuscriptFromState, loadAndDispatchManuscripts, sendManuscriptToApi } from "../utils/manuscript";
import * as toastr from "toastr";

const mapStateToProps = (state, { match }) => {
  let manuscriptFromState = getManuscriptFromState(state, parseInt(match.params.manuscriptId, 10));
  return {
    manuscript: manuscriptFromState,
    manuscripts: state.manuscripts
  };
};

const mapDispatchToProps = (dispatch, { history, match }) => {
  dispatch(loadManuscript(match.params.manuscriptId));
  fetch(getManuscriptApiUrl(match.params.manuscriptId))
    .then(response => response.json())
    .then(manuscript => dispatch(loadManuscript(match.params.manuscriptId, manuscript)))
    .catch(error => dispatch(loadManuscript(match.params.manuscriptId, error)))
    .then(() => loadAndDispatchManuscripts(dispatch));
  const manuscriptId = parseInt(match.params.manuscriptId, 10);
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem(manuscriptId));
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(manuscriptId, propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(manuscriptId, order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      if (window.confirm('Are you sure?')) {
        dispatch(deleteManuscriptItem(manuscriptId, order));
      }
    },
    moveManuscriptItemDown: (order) => {
      dispatch(moveManuscriptItem(manuscriptId, order, 1));
    },
    moveManuscriptItemUp: (order) => {
      dispatch(moveManuscriptItem(manuscriptId, order, -1));
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
    },
    onTabSelect: (key) => {
      history.push(`/edit/${manuscriptId}/?tab=${key}`)
    }
  }
};

const EditManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default EditManuscript;
