import { ADD_MANUSCRIPT_ITEM } from "../current_manuscript";
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

export default function addManuscriptItem(state, action) {
  const order = state.items.length + 1;
  return {
    ...state,
    items: [
      ...state.items,
      manuscriptItem({}, {
        ...action,
        order
      })
    ]
  };
}
