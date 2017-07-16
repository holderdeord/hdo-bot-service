import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";
import { editManuscript } from "../actions/manuscripts";
import { getManuscriptApiUrl } from "../utils/urls";
import { loadAndDispatchManuscripts, sendManuscriptToApi } from "../utils/manuscript";
import * as toastr from "toastr";
import {
  addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty, deleteManuscriptItem,
  loadManuscript, moveManuscriptItem
} from "../actions/current_manuscript";

const mapStateToProps = (state) => {
  return {
    manuscript: state.current_manuscript,
    manuscripts: state.manuscripts
  };
};

const mapDispatchToProps = (dispatch, { history, match }) => {
  dispatch(loadManuscript());
  fetch(getManuscriptApiUrl(match.params.manuscriptId))
    .then(response => response.json())
    .then(manuscript => dispatch(loadManuscript(manuscript)))
    .catch(error => dispatch(loadManuscript(error)));
  loadAndDispatchManuscripts(dispatch);
  const manuscriptId = parseInt(match.params.manuscriptId, 10);
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem());
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(propertyName, event.target.value));
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(order, propertyName, event.target.value));
    },
    deleteManuscriptItem: (order) => {
      if (window.confirm('Are you sure?')) {
        dispatch(deleteManuscriptItem(order));
      }
    },
    moveManuscriptItemDown: (order) => {
      dispatch(moveManuscriptItem(order, 1));
    },
    moveManuscriptItemUp: (order) => {
      dispatch(moveManuscriptItem(order, -1));
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
