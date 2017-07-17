export default function loadManuscripts(state, action) {
  if (!action.manuscripts) {
    return state;
  }
  return [...action.manuscripts];
}