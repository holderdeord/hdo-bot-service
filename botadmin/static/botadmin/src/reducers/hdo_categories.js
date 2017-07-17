export const LOAD_HDO_CATEGORIES = 'LOAD_HDO_CATEGORIES';

const hdo_categories = (state = [], action) => {
  switch (action.type) {
    case LOAD_HDO_CATEGORIES:
      if (!action.categories) {
        return state;
      }
      return [...action.categories];
    default:
      return state;
  }
};

export default hdo_categories;
