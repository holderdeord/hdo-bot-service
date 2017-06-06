export default function moveManuscriptItem(state, action) {
  const selectedManuscript = state.find(manuscript => manuscript.pk === action.manuscriptId);
  const selectedManuscriptIndex = state.indexOf(selectedManuscript);
  const selectedItemA = selectedManuscript.items.find(item => item.order === action.order);
  const selectedItemAIndex = selectedManuscript.items.indexOf(selectedItemA);
  selectedManuscript.items.splice(selectedItemAIndex, 1);
  const selectedItemB = selectedManuscript.items.find(item => item.order === action.order + action.move);
  const selectedItemBIndex = selectedManuscript.items.indexOf(selectedItemB);
  selectedManuscript.items.splice(selectedItemBIndex, 1);
  const newManuscript = {
    ...selectedManuscript,
    items: [
      ...selectedManuscript.items,
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
  state.splice(selectedManuscriptIndex, 1, newManuscript);
  return [...state];
}
