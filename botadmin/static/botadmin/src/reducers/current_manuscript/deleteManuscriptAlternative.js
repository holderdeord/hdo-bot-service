export default function deleteManuscriptAlternative(state, alternativeIndex) {
  const voter_guide_alternatives = [...state.voter_guide_alternatives];
  const alternative = voter_guide_alternatives.splice(alternativeIndex, 1)[0];
  const voter_guide_parties = [...state.voter_guide_parties];
  alternative.parties.forEach(party => {
    const partyIndex = voter_guide_alternatives.indexOf(party);
    voter_guide_parties.splice(partyIndex, 1);
  });
  return {
    ...state,
    has_changes: true,
    voter_guide_alternatives,
    voter_guide_parties
  };
}
