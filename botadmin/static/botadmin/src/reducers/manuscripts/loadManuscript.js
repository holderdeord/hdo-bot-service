export default function loadManuscript(state, action) {
  if (!action.manuscript) {
    return state;
  }
  const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  if (selectedManuscript) {
    return state;
  }
  return [...state, {
    pk: action.manuscriptId,
    name: action.manuscript.name,
    type: action.manuscript.type,
    items: action.manuscript.items
  }];
}
