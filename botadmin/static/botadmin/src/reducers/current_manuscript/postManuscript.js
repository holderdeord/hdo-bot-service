export default function postManuscript(state, { json }) {
  if (!json || json.message) {
    return state;
  }
  return {
    ...json,
    has_changes: false,
    items: [...json.items],
    voter_guide_alternatives: [...json.voter_guide_alternatives],
    voter_guide_parties: []
  };
}
