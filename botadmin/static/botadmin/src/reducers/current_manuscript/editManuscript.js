import { getPartiesFromAlternatives } from '../../utils/manuscript';
export default function editManuscript(state, { json }) {
  if (!json || json.message) {
    return state;
  }
  return {
    ...json,
    has_changes: false,
    voter_guide_parties: getPartiesFromAlternatives(json.voter_guide_alternatives)
  };
}