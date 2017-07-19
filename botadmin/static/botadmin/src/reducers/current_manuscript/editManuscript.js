export default function editManuscript(state, { json }) {
  if (!json || json.message) {
    return state;
  }
  return { ...json };
}