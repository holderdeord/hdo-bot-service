export default function loadManuscript(state, { json }) {
  if (!json || json.message) {
    return state;
  }
  return {
    ...json,
    voter_guide_parties: [...new Set(json.voter_guide_alternatives.reduce((memo, alternative) => memo.concat(alternative.parties), []))]
  };
  // const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  // if (selectedManuscript) {
  //   const selectedIndex = state.indexOf(selectedManuscript);
  //   return [...state.splice(selectedIndex, 1, selectedManuscript)];
  // }
  // return [...state, {...action.json}];
}

