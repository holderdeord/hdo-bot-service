export default class CoreManuscript {
  constructor(name = '', items = []) {
    this.name = name;
    this.items = items;
  }

  addItem() {
    const order = this.items[this.items.length - 1].order + 1;
    this.items.push({
      order,
      text: '',
      type: 'text'
    });
  }
}
