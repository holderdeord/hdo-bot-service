export default function loadManuscripts(state, action) {
  if (!action.manuscripts) {
    return state;
  }
  const existingIds = state.map(x => x.pk);
  return [...state, ...action.manuscripts.filter(x => existingIds.indexOf(x.pk) === -1)];
}