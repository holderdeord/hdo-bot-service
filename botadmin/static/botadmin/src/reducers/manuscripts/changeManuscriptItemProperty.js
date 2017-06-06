export default function changeManuscriptItemProperty(state, action) {
  const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  if (!selectedManuscript) {
    return state;
  }
  const indexOfManuscript = state.indexOf(selectedManuscript);
  const selectedItem = selectedManuscript.items.find(item => item.order === action.order);
  if (!selectedItem) {
    return state;
  }
  selectedItem[action.propertyName] = action.value;
  const newManuscript = {
    ...selectedManuscript,
    items: [...selectedManuscript.items]
  };
  state.splice(indexOfManuscript, 1, newManuscript);
  return [...state];
}
