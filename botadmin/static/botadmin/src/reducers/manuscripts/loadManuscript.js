export default function loadManuscript(state, action) {
  if (!action.manuscript) {
    return state;
  }
  const selectedManuscript = state.find(manuscript => manuscript.id === action.manuscriptId);
  if (selectedManuscript) {
    return state;
  }
  return [...state, {
    id: action.manuscriptId,
    name: action.manuscript.name,
    type: 'info',
    items: action.manuscript.items
  }];
}
