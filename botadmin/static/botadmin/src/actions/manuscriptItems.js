// import { ADD_MANUSCRIPT_ITEM, DELETE_MANUSCRIPT_ITEM } from "../reducers/manuscriptItems";
//
// let nextOrderNo = 1;
//
// export const addManuscriptItem = (itemType = 'text', itemText = 'Heisann') => {
//   return {
//     type: ADD_MANUSCRIPT_ITEM,
//     order: nextOrderNo++,
//     itemType,
//     itemText
//   };
// };
//
// export const deleteManuscriptItem = (order) => {
//   nextOrderNo--;
//   return {
//     type: DELETE_MANUSCRIPT_ITEM,
//     order
//   };
// };