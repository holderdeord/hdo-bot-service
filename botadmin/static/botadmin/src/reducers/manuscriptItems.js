// export const ADD_MANUSCRIPT_ITEM = 'ADD_MANUSCRIPT_ITEM';
// export const DELETE_MANUSCRIPT_ITEM = 'DELETE_MANUSCRIPT_ITEM';
//
// const manuscriptItem = (state = {}, action) => {
//   switch (action.type) {
//     case ADD_MANUSCRIPT_ITEM:
//       return {
//         order: action.order,
//         text: action.itemText,
//         type: action.itemType
//       };
//
//     default:
//       return state
//   }
// };
//
// const manuscriptItems = (state = [], action) => {
//   switch (action.type) {
//     case ADD_MANUSCRIPT_ITEM:
//       return [
//         ...state,
//         manuscriptItem(undefined, action)
//       ];
//     case DELETE_MANUSCRIPT_ITEM:
//       return state
//         .filter(item => item.order !== action.order)
//         .map((item, index) => {
//           item.order = index + 1;
//           return item;
//         });
//     default:
//       return state
//   }
// };
//
// export default manuscriptItems;