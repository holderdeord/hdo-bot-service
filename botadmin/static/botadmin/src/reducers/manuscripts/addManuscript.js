import { ADD_MANUSCRIPT } from "../manuscripts";
const manuscript = (state = {}, action) => {
  switch (action.type) {
    case ADD_MANUSCRIPT:
      return {
        id: action.id,
        name: action.name,
        type: action.manuscriptType,
        items: action.items
      };

    default:
      return state
  }
};

export default function addManuscript (state, action) {
  return [
    ...state,
    manuscript(undefined, action)
  ];
}
