export function createManuscriptPayload(manuscript) {
  return JSON.stringify({
    pk: manuscript.pk,
    type: manuscript.type,
    name: manuscript.name,
    items: manuscript.items.map(item => {
      return {
        type: item.type,
        order: item.order,
        text: item.text,
        reply_action_1: item.reply_action_1,
        reply_action_2: item.reply_action_2,
        reply_action_3: item.reply_action_3,
        reply_text_1: item.reply_text_1,
        reply_text_2: item.reply_text_2,
        reply_text_3: item.reply_text_3
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