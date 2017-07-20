export default function addPromiseToAlternative(state, alternativeIndex, promise, promiseId) {
  const voter_guide_alternatives = [...state.voter_guide_alternatives];
  const alternative = voter_guide_alternatives[alternativeIndex];
  alternative.full_promises.push({
    pk: promiseId,
    body: promise.body,
    promisor_name: promise.promisor_name
  });
  alternative.promises.push(promiseId);
  alternative.parties.push(promise.promisor_name);
  return {
    ...state,
    has_changes: true,
    voter_guide_alternatives
  };
}