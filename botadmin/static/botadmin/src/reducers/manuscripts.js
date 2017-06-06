import addManuscriptItem from "./manuscripts/addManuscriptItem";
import deleteManuscriptItem from "./manuscripts/deleteManuscriptItem";
import addManuscript from "./manuscripts/addManuscript";
import changeManuscriptProperty from "./manuscripts/changeManuscriptProperty";
import postManuscript from "./manuscripts/postManuscript";
import changeManuscriptItemProperty from "./manuscripts/changeManuscriptItemProperty";

export const ADD_MANUSCRIPT = 'ADD_MANUSCRIPT';
export const ADD_MANUSCRIPT_ITEM = 'ADD_MANUSCRIPT_ITEM';
export const CHANGE_MANUSCRIPT_ITEM_PROPERTY = 'CHANGE_MANUSCRIPT_ITEM_PROPERTY';
export const CHANGE_MANUSCRIPT_PROPERTY = 'CHANGE_MANUSCRIPT_PROPERTY';
export const DELETE_MANUSCRIPT_ITEM = 'DELETE_MANUSCRIPT_ITEM';
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
    case POST_MANUSCRIPT:
      return postManuscript(state, action);
    default:
      return state
  }
};

export default manuscripts;