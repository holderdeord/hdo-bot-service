import ManuscriptForm from "../components/ManuscriptForm";
import { connect } from "react-redux";
import {
  postManuscript
} from "../actions/manuscripts";
import { loadAndDispatchManuscripts, sendManuscriptToApi } from "../utils/manuscript";
import { getManuscriptsApiUrl } from "../utils/urls";
import * as toastr from "toastr";
import {
  addManuscriptItem, changeManuscriptItemProperty, changeManuscriptProperty,
  createManuscript, deleteManuscriptItem, moveManuscriptItem
} from "../actions/current_manuscript";

const mapStateToProps = (state) => {
  return {
    manuscript: state.current_manuscript,
    manuscripts: state.manuscripts
  };
};

const mapDispatchToProps = (dispatch, { history }) => {
  dispatch(createManuscript());
  dispatch(addManuscriptItem());
  loadAndDispatchManuscripts(dispatch);
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
          dispatch(postManuscript(manuscript, error));
          toastr.error('Failed to create manuscript');
        });
    },
    onTabSelect: (key) => {
      history.push(`/create?tab=${key}`)
    }
  }
};

const CreateManuscript = connect(
  mapStateToProps,
  mapDispatchToProps
)(ManuscriptForm);

export default CreateManuscript;
