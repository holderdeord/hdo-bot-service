import { LOAD_HDO_CATEGORIES } from "../reducers/hdo_categories";

export const loadHdoCategories = (categories) => {
  return {
    type: LOAD_HDO_CATEGORIES,
    categories
  };
};
