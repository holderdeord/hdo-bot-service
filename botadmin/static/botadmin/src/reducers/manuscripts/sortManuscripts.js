export default function sortManuscripts(state, action) {
  if (!action.fieldName) {
    return state;
  }
  const sortedList = state.sort((a, b) => b[ action.fieldName ] !== null ?
    (a[ action.fieldName ] > b[ action.fieldName ] ? 1 : -1) :
    -1
  );
  return [ ...sortedList ];
}
