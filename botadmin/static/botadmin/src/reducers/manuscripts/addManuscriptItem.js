import { ADD_MANUSCRIPT_ITEM } from "../manuscripts";
const manuscriptItem = (state = {}, action) => {
  switch (action.type) {
    case ADD_MANUSCRIPT_ITEM:
      return {
        order: action.order,
        text: action.itemText,
        type: action.itemType
      };

    default:
      return state
  }
};

export default function addManuscriptItem (state, action) {
  const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  if (!selectedManuscript) {
    return state;
  }
  const indexOfManuscript = state.indexOf(selectedManuscript);
  const order = selectedManuscript.items.length + 1;
  const newManuscript = {
    ...selectedManuscript,
    items: [
      ...selectedManuscript.items,
      manuscriptItem({}, {
        ...action,
        order
      })
    ]
  };
  state.splice(indexOfManuscript, 1, newManuscript);
  return [...state];
}
