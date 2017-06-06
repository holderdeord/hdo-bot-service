export default function editManuscript(state, action) {
  if (!action.json || action.json.message) {
    return state;
  }
  const oldManuscript = state.find(manuscript => manuscript.id === -1);
  const oldManuscriptIndex = state.indexOf(oldManuscript);
  const newManuscript = {
    ...action.json,
    id: action.json.pk,
    items: [...action.json.items]
  };
  state.splice(oldManuscriptIndex, 1, newManuscript);
  return [...state];
}