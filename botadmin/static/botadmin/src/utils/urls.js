const apiUrl = 'http://localhost:8000/api';

export function getManuscriptApiUrl(manuscriptId) {
  return `${apiUrl}/manuscripts/${manuscriptId}/`;
}

export function getManuscriptsApiUrl() {
  return `${apiUrl}/manuscripts/`;
}
