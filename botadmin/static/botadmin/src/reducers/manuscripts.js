import addManuscriptItem from "./manuscripts/addManuscriptItem";
import deleteManuscriptItem from "./manuscripts/deleteManuscriptItem";
import addManuscript from "./manuscripts/addManuscript";
import changeManuscriptProperty from "./manuscripts/changeManuscriptProperty";
import postManuscript from "./manuscripts/postManuscript";
import changeManuscriptItemProperty from "./manuscripts/changeManuscriptItemProperty";
import editManuscript from "./manuscripts/editManuscript";
import loadManuscript from "./manuscripts/loadManuscript";
import loadManuscripts from "./manuscripts/loadManuscripts";

export const ADD_MANUSCRIPT = 'ADD_MANUSCRIPT';
export const ADD_MANUSCRIPT_ITEM = 'ADD_MANUSCRIPT_ITEM';
export const CHANGE_MANUSCRIPT_ITEM_PROPERTY = 'CHANGE_MANUSCRIPT_ITEM_PROPERTY';
export const CHANGE_MANUSCRIPT_PROPERTY = 'CHANGE_MANUSCRIPT_PROPERTY';
export const DELETE_MANUSCRIPT_ITEM = 'DELETE_MANUSCRIPT_ITEM';
export const DELETE_MANUSCRIPT = 'DELETE_MANUSCRIPT';
export const EDIT_MANUSCRIPT = 'EDIT_MANUSCRIPT';
export const LOAD_MANUSCRIPT = 'LOAD_MANUSCRIPT';
export const LOAD_MANUSCRIPTS = 'LOAD_MANUSCRIPTS';
export const POST_MANUSCRIPT = 'POST_MANUSCRIPT';

const manuscripts = (state = [], action) => {
  switch (action.type) {
    case ADD_MANUSCRIPT:
      return addManuscript(state, action);
    case ADD_MANUSCRIPT_ITEM:
      return addManuscriptItem(state, action);
    case CHANGE_MANUSCRIPT_ITEM_PROPERTY:
      return changeManuscriptItemProperty(state, action);
    case CHANGE_MANUSCRIPT_PROPERTY:
      return changeManuscriptProperty(state, action);
    case DELETE_MANUSCRIPT_ITEM:
      return deleteManuscriptItem(state, action);
    case EDIT_MANUSCRIPT:
      return editManuscript(state, action);
    case LOAD_MANUSCRIPT:
      return loadManuscript(state, action);
    case LOAD_MANUSCRIPTS:
      return loadManuscripts(state, action);
    case POST_MANUSCRIPT:
      return postManuscript(state, action);
    default:
      return state
  }
};

export default manuscripts;