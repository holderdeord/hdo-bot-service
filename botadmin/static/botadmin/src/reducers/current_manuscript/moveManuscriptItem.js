export default function moveManuscriptItem(state, action) {
  const selectedItemA = state.items.find(item => item.order === action.order);
  const selectedItemAIndex = state.items.indexOf(selectedItemA);
  state.items.splice(selectedItemAIndex, 1);
  const selectedItemB = state.items.find(item => item.order === action.order + action.move);
  const selectedItemBIndex = state.items.indexOf(selectedItemB);
  state.items.splice(selectedItemBIndex, 1);
  return {
    ...state,
    has_changes: true,
    items: [
      ...state.items,
      {
        ...selectedItemA,
        order: action.order + action.move
      },
      {
        ...selectedItemB,
        order: action.order
      }
    ].sort((itemA, itemB) => itemA.order > itemB.order)
  };
}
