export default function loadManuscript(state, action) {
  if (!action.json || action.json.message) {
    return state;
  }
  const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  if (selectedManuscript) {
    return state;
  }
  return [...state, {...action.json}];
}
