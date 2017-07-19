export default function postManuscript(state, { json }) {
  if (!json || json.message) {
    return state;
  }
  return {
    ...json,
    items: [...json.items],
    voter_guide_alternatives: [...json.voter_guide_alternatives]
  };
}
