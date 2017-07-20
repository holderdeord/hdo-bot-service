export default function changeManuscriptProperty(state, action) {
  state[action.propertyName] = action.value;
  return {
    ...state,
    has_changes: true,
    items: [...state.items]
  };
}
