export default function changeManuscriptAlternativeProperty(state, { index, propertyName, value }) {
  const selectedAlternative = state.voter_guide_alternatives[index];
  if (!selectedAlternative) {
    return state;
  }
  const alternative = {
    ...selectedAlternative,
    [propertyName]: value
  };
  const voter_guide_alternatives = [...state.voter_guide_alternatives];
  voter_guide_alternatives.splice(index, 1, alternative);
  return {
    ...state,
    voter_guide_alternatives
  };
}
