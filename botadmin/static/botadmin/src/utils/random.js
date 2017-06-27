export function generateRandomString(numberOfCharacters = 5) {
  return Math.random().toString(36).substr(2, numberOfCharacters);
}