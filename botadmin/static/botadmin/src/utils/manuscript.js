export function createManuscriptPayload(manuscript) {
  return JSON.stringify({
    pk: manuscript.pk,
    name: manuscript.name,
    items: manuscript.items.map(item => {
      return {
        type: item.type,
        order: item.order,
        text: item.text
      };
    })
  });
}

export function getManuscriptFromState(state, manuscriptId) {
  return state.manuscripts.find(manuscript => manuscript.pk === manuscriptId) || {
      pk: manuscriptId,
      name: '',
      type: 'info',
      items: []
    };
}

export function sendManuscriptToApi(manuscript, url, method) {
  return fetch(url, {
    method: method,
    body: createManuscriptPayload(manuscript),
    headers: new Headers({
      'Content-Type': 'application/json'
    })
  })
    .then(response => response.json());
}