export default function changeManuscriptProperty(state, action) {
  state[action.propertyName] = action.value;
  return {
    ...state,
    items: [...state.items]
  };
}
