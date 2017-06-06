export default function postManuscript(state, action) {
  const manuscript = state.find(manuscript => manuscript.id === action.manuscriptId);
  if (!manuscript) {
    return state;
  }

  return state;
}
