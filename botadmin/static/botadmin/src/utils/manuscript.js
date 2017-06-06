export function createManuscriptPayload(manuscript) {
  return {
    pk: manuscript.id,
    name: manuscript.name,
    items: manuscript.items.map(item => {
      return {
        type: item.type,
        order: item.order,
        text: item.text
      };
    })
  };
}
