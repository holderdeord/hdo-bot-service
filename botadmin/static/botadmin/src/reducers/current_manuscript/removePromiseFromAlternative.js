export default function removePromiseFromAlternative(state, alternativeIndex, promise) {
  const voter_guide_alternatives = [...state.voter_guide_alternatives];
  const alternative = voter_guide_alternatives[alternativeIndex];
  // removing promise
  const promiseIndex = alternative.promises.indexOf(promise.pk);
  alternative.promises.splice(promiseIndex, 1);
  // removing full_promise
  const fullPromiseIndex = alternative.full_promises.indexOf(promise);
  alternative.full_promises.splice(fullPromiseIndex, 1);
  // removing promisor_name from parties
  const voter_guide_parties = [...state.voter_guide_parties];
  const partyIndex = voter_guide_parties.indexOf(promise.promisor_name);
  voter_guide_parties.splice(partyIndex, 1);
  return {
    ...state,
    voter_guide_alternatives,
    voter_guide_parties
  };
}
