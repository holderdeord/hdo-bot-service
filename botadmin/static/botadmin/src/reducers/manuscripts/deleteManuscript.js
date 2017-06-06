export default function deleteManuscript(state, action) {
  if (action.json && action.json.status === 204) {
    const selectedManuscript = state.find(manuscript => manuscript.id === action.manuscriptId);
    const selectedIndex = state.indexOf(selectedManuscript);
    state.splice(selectedIndex, 1);
    return [...state];
  }
  return state;
}