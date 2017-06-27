const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export function getManuscriptApiUrl(manuscriptId) {
  return `${apiUrl}/manuscripts/${manuscriptId}/`;
}

export function getManuscriptsApiUrl() {
  return `${apiUrl}/manuscripts/`;
}
