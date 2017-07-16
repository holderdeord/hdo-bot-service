export default function loadManuscript(state, action) {
  if (!action.json || action.json.message) {
    return state;
  }
  return action.json;
  // const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  // if (selectedManuscript) {
  //   const selectedIndex = state.indexOf(selectedManuscript);
  //   return [...state.splice(selectedIndex, 1, selectedManuscript)];
  // }
  // return [...state, {...action.json}];
}

