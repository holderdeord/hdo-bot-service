import loadManuscript from "./current_manuscript/loadManuscript";

export const CREATE_MANUSCRIPT = 'CREATE_MANUSCRIPT';
export const LOAD_MANUSCRIPT = 'LOAD_MANUSCRIPT';

const current_manuscript = (state = create_manuscript(), action) => {
  switch (action.type) {
    case CREATE_MANUSCRIPT:
      return create_manuscript();
    case LOAD_MANUSCRIPT:
      return loadManuscript(state, action);
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
      voter_guide_alternatives: []
    };
}
