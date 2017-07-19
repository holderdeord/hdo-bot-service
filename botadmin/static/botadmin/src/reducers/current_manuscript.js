import loadManuscript from "./current_manuscript/loadManuscript";
import addManuscriptItem from "./current_manuscript/addManuscriptItem";
import changeManuscriptItemProperty from "./current_manuscript/changeManuscriptItemProperty";
import changeManuscriptProperty from "./current_manuscript/changeManuscriptProperty";
import deleteManuscriptItem from "./current_manuscript/deleteManuscriptItem";
import moveManuscriptItem from "./current_manuscript/moveManuscriptItem";
import changeManuscriptAlternativeProperty from "./current_manuscript/changeManuscriptAlternativeProperty";
import postManuscript from "./current_manuscript/postManuscript";
import editManuscript from "./current_manuscript/editManuscript";

export const ADD_MANUSCRIPT_ITEM = 'ADD_MANUSCRIPT_ITEM';
export const CHANGE_MANUSCRIPT_ALTERNATIVE_PROPERTY = 'CHANGE_MANUSCRIPT_ALTERNATIVE_PROPERTY';
export const CHANGE_MANUSCRIPT_ITEM_PROPERTY = 'CHANGE_MANUSCRIPT_ITEM_PROPERTY';
export const CHANGE_MANUSCRIPT_PROPERTY = 'CHANGE_MANUSCRIPT_PROPERTY';
export const CREATE_MANUSCRIPT = 'CREATE_MANUSCRIPT';
export const DELETE_MANUSCRIPT_ITEM = 'DELETE_MANUSCRIPT_ITEM';
export const EDIT_MANUSCRIPT = 'EDIT_MANUSCRIPT';
export const LOAD_MANUSCRIPT = 'LOAD_MANUSCRIPT';
export const MOVE_MANUSCRIPT_ITEM = 'MOVE_MANUSCRIPT_ITEM';
export const POST_MANUSCRIPT = 'POST_MANUSCRIPT';

const current_manuscript = (state = create_manuscript(), action) => {
  switch (action.type) {
    case ADD_MANUSCRIPT_ITEM:
      return addManuscriptItem(state, action);
    case CHANGE_MANUSCRIPT_ALTERNATIVE_PROPERTY:
      return changeManuscriptAlternativeProperty(state, action);
    case CHANGE_MANUSCRIPT_ITEM_PROPERTY:
      return changeManuscriptItemProperty(state, action);
    case CHANGE_MANUSCRIPT_PROPERTY:
      return changeManuscriptProperty(state, action);
    case CREATE_MANUSCRIPT:
      return create_manuscript();
    case DELETE_MANUSCRIPT_ITEM:
      return deleteManuscriptItem(state, action);
    case EDIT_MANUSCRIPT:
      return editManuscript(state, action);
    case LOAD_MANUSCRIPT:
      return loadManuscript(state, action);
    case MOVE_MANUSCRIPT_ITEM:
      return moveManuscriptItem(state, action);
    case POST_MANUSCRIPT:
      return postManuscript(state, action);
    default:
      return state;
  }
};

export default current_manuscript;

function create_manuscript() {
  return {
    pk: null,
    name: '',
    type: 'info',
    items: [],
    voter_guide_alternatives: [],
    is_first_in_category: false,
    is_defualt: false
  };
}
