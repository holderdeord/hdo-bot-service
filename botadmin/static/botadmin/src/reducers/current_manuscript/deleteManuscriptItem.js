export default function deleteManuscriptItem (state, action) {
  const selectedItem = state.items.find(item => item.order === action.order);
  if (!selectedItem) {
    return state;
  }
  const indexOfItem = state.items.indexOf(selectedItem);
  state.items.splice(indexOfItem, 1);
  state.items.forEach((item, index) => {
    item.order = index + 1;
  });
  return {
    ...state,
    items: [...state.items]
  };
}
