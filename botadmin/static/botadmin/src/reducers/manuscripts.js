import postManuscript from "./manuscripts/postManuscript";
import editManuscript from "./manuscripts/editManuscript";
import loadManuscripts from "./manuscripts/loadManuscripts";
import deleteManuscript from "./manuscripts/deleteManuscript";

export const DELETE_MANUSCRIPT = 'DELETE_MANUSCRIPT';
export const EDIT_MANUSCRIPT = 'EDIT_MANUSCRIPT';
export const LOAD_MANUSCRIPTS = 'LOAD_MANUSCRIPTS';
export const POST_MANUSCRIPT = 'POST_MANUSCRIPT';

const manuscripts = (state = [], action) => {
  switch (action.type) {
    case DELETE_MANUSCRIPT:
      return deleteManuscript(state, action);
    case EDIT_MANUSCRIPT:
      return editManuscript(state, action);
    case LOAD_MANUSCRIPTS:
      return loadManuscripts(state, action);
    case POST_MANUSCRIPT:
      return postManuscript(state, action);
    default:
      return state
  }
};

export default manuscripts;