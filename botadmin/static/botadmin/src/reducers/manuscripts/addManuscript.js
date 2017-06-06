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
  const selectedManuscript = state.find(manuscript => manuscript.id === action.id);
  if (selectedManuscript) {
    return state;
  }
  return [
    ...state,
    manuscript(undefined, action)
  ];
}
