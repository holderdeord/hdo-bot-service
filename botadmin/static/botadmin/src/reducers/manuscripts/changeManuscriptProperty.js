export default function changeManuscriptProperty(state, action) {
  const selectedManuscript = state.find(manuscript => manuscript.id === action.manuscriptId);
  if (!selectedManuscript) {
    return state;
  }
  const indexOfManuscript = state.indexOf(selectedManuscript);
  selectedManuscript[action.propertyName] = action.value;
  const newManuscript = {
    ...selectedManuscript,
    items: [...selectedManuscript.items]
  };
  state.splice(indexOfManuscript, 1, newManuscript);
  return [...state];
}
