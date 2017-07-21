export default function addManuscriptAlternative(state) {
  const voter_guide_alternatives = [
    ...state.voter_guide_alternatives,
    {
      text: null,
      full_promises: [],
      promises: [],
      parties: []
    }
  ];
  return {
    ...state,
    voter_guide_alternatives
  };
}