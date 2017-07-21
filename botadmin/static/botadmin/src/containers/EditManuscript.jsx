import { connect } from "react-redux";
import ManuscriptForm from "../components/ManuscriptForm";
import { getManuscriptApiUrl } from "../utils/urls";
import { loadAndDispatchManuscripts, sendManuscriptToApi } from "../utils/manuscript";
import * as toastr from "toastr";
import {
  addManuscriptAlternative,
  addManuscriptItem, addPromiseToAlternative, changeManuscriptAlternativeProperty, changeManuscriptItemProperty,
  changeManuscriptProperty,
  deleteManuscriptItem, editManuscript, moveManuscriptItem, removePromiseFromAlternative
} from "../actions/current_manuscript";
import { loadAndDispatchHdoCategories } from "../utils/hdo_categories";
import { loadAndDispatchManuscript } from "../utils/current_manuscript";
import { getTabId } from "../utils/getTabId";
import { handleAndDispatchPromisesModal } from "../utils/handleAndDispatchPromisesModal";

const mapStateToProps = (state) => {
  return {
    hdo_categories: state.hdo_categories,
    manuscript: state.current_manuscript,
    manuscripts: state.manuscripts,
    promises_modal: state.promises_modal
  };
};

const mapDispatchToProps = (dispatch, ownProps) => {
  const {
    history,
    match
  } = ownProps;
  loadAndDispatchManuscript(dispatch, match.params.manuscriptId);
  loadAndDispatchManuscripts(dispatch);
  loadAndDispatchHdoCategories(dispatch);
  const manuscriptId = parseInt(match.params.manuscriptId, 10);
  handleAndDispatchPromisesModal(dispatch, match);
  return {
    addManuscriptAlternative: () => {
      dispatch(addManuscriptAlternative())
    },
    addManuscriptItem: () => {
      dispatch(addManuscriptItem());
    },
    addPromise: (alternativeIndex, promise, promiseId) => {
      dispatch(addPromiseToAlternative(alternativeIndex, promise, parseInt(promiseId, 10)));
      history.push(`/edit/${manuscriptId}/${getTabId(match)}/`);
    },
    changeManuscriptProperty: (event, propertyName) => {
      dispatch(changeManuscriptProperty(propertyName, event.target.value));
    },
    changeManuscriptAlternativeProperty: (event, index, propertyName) => {
      dispatch(changeManuscriptAlternativeProperty(index, propertyName, event.target.value))
    },
    changeManuscriptItemProperty: (event, order, propertyName) => {
      dispatch(changeManuscriptItemProperty(order, propertyName, event.target.value));
    },
    closePromisesModal: () => {
      history.push(`/edit/${manuscriptId}/${getTabId(match)}/`);
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
          console.error(error);
          dispatch(editManuscript(manuscript, error));
          toastr.error('Failed to save manuscript');
        });
    },
    onTabSelect: (key) => {
      history.push(`/edit/${manuscriptId}/${key}/`)
    },
    openPromisesModal: (index) => {
      history.push(`/edit/${manuscriptId}/${getTabId(match)}/${index}/`);
    },
    removePromiseFromAlternative: (alternativeIndex, promise) => {
      if (window.confirm('Are you sure?')) {
        dispatch(removePromiseFromAlternative(alternativeIndex, promise));
      }
    }
  }
};

const EditManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default EditManuscript;
