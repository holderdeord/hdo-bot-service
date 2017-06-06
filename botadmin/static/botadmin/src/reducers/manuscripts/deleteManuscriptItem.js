export default function deleteManuscriptItem (state, action) {
  const selectedManuscript = state.find(manuscript => manuscript.id === action.manuscriptId);
  if (!selectedManuscript) {
    return state;
  }
  const indexOfManuscript = state.indexOf(selectedManuscript);
  const selectedItem = selectedManuscript.items.find(item => item.order === action.order);
  if (!selectedItem) {
    return state;
  }
  const indexOfItem = selectedManuscript.items.indexOf(selectedItem);
  selectedManuscript.items.splice(indexOfItem, 1);
  selectedManuscript.items.forEach((item, index) => {
    item.order = index + 1;
  });
  const newManuscript = {
    ...selectedManuscript,
    items: [...selectedManuscript.items]
  };
  state.splice(indexOfManuscript, 1, newManuscript);
  return [...state];
}
