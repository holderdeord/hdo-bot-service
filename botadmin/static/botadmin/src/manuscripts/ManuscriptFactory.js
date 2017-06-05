import InfoManuscript from "./InfoManuscript";
export default class ManuscriptFactory {
  loadManuscript(manuscriptData) {
    return new InfoManuscript(manuscriptData.name, manuscriptData.items);
  }
}