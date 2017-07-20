import ManuscriptForm from "../components/ManuscriptForm";
import { connect } from "react-redux";
import { loadAndDispatchManuscripts, sendManuscriptToApi } from "../utils/manuscript";
import { getManuscriptsApiUrl } from "../utils/urls";
import * as toastr from "toastr";
import {
  addManuscriptItem, changeManuscriptAlternativeProperty, changeManuscriptItemProperty, changeManuscriptProperty,
  deleteManuscriptItem, moveManuscriptItem, postManuscript
} from "../actions/current_manuscript";
import { loadAndDispatchHdoCategories } from "../utils/hdo_categories";
import { createAndDispatchManuscript } from "../utils/current_manuscript";
import { closePromisesModal, openPromisesModal } from "../actions/promises_modal";
import { handleAndDispatchPromisesModal } from "../utils/handleAndDispatchPromisesModal";
import { getTabId } from "../utils/getTabId";

const mapStateToProps = (state) => {
  return {
    hdo_categories: state.hdo_categories,
    manuscript: state.current_manuscript,
    manuscripts: state.manuscripts,
    promises_modal: state.promises_modal
  };
};

const mapDispatchToProps = (dispatch, {
  history,
  match
}) => {
  createAndDispatchManuscript(dispatch);
  loadAndDispatchManuscripts(dispatch);
  loadAndDispatchHdoCategories(dispatch);
  handleAndDispatchPromisesModal(dispatch, match);
  return {
    addManuscriptItem: () => {
      dispatch(addManuscriptItem());
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
    closePromisesModal: () => history.push(`/create/${getTabId(match)}`),
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
      dispatch(postManuscript(manuscript));
      const timeoutHandleId = setTimeout(() => toastr.info('Trying to save manuscript, please wait'), 300);
      return sendManuscriptToApi(manuscript, getManuscriptsApiUrl(), 'POST')
        .then(createdManuscript => {
          clearTimeout(timeoutHandleId);
          dispatch(postManuscript(manuscript, createdManuscript));
          history.push(`/edit/${createdManuscript.pk}`);
          toastr.success('Successfully created manuscript, navigated you to edit-mode');
        })
        .catch(error => {
          console.error(error);
          dispatch(postManuscript(manuscript, error));
          toastr.error('Failed to create manuscript');
        });
    },
    onTabSelect: (key) => history.push(`/create/${key}/`),
    openPromisesModal: (index) => history.push(`/create/${getTabId(match)}/${index}`),
  }
};

const CreateManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default CreateManuscript;
