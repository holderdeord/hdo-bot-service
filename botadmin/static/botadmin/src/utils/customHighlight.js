export const customHighlight = {
  pre_tags: ['<mark>'],
  post_tags: ['</mark>'],
  fields: {
    body: {
      fragment_size: 800 // longest promise is ~600 chars
    }
  }
};
