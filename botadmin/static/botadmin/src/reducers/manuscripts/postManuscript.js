export default function postManuscript(state, action) {
  const selectedManuscript = state.find(manuscript => manuscript.id === action.manuscriptId);
  if (!selectedManuscript) {
    return state;
  }
  console.log('posting manuscript', selectedManuscript);
  return state;
}
