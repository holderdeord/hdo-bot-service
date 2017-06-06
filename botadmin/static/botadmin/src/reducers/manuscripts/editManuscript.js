export default function editManuscript(state, action) {
  if (!action.json || action.json.message) {
    return state;
  }
  return state;
  // const oldManuscript = state.find(manuscript => parseInt(manuscript.id, 10) === action.json.pk);
  // console.log(oldManuscript, state, action);
  // const oldManuscriptIndex = state.indexOf(oldManuscript);
  // const newManuscript = {
  //   ...action.json,
  //   id: action.json.pk,
  //   items: [...action.json.items]
  // };
  // state.splice(oldManuscriptIndex, 1, newManuscript);
  // return [...state];
}