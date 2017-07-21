import { getPartiesFromAlternatives } from "../../utils/manuscript";
export default function loadManuscript(state, { json }) {
  if (!json || json.message) {
    return state;
  }
  // let numberOfPromisesFromUser = getNumberOfPromises(state.voter_guide_alternatives);
  // let numberOfPromisesFromApi = getNumberOfPromises(json.voter_guide_alternatives);
  // let has_changes = numberOfPromisesFromUser > numberOfPromisesFromApi;
  return state.pk === json.pk && state.has_changes ?
    state :
    {
      ...json,
      has_changes: false,
      voter_guide_parties: getPartiesFromAlternatives(json.voter_guide_alternatives)
    };
}

// function getNumberOfPromises(voter_guide_alternatives) {
//   return voter_guide_alternatives.reduce((memo, alternative) => memo + alternative.promises.length, 0);
// }