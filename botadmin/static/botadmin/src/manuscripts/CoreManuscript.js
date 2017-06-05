export default class CoreManuscript {
  constructor(name = '', items = [ { order: 1, text: 'Heisann!', type: 'text' } ]) {
    this.name = name;
    this.items = items;
  }

  addItem() {
    const order = this.items[ this.items.length - 1 ].order + 1;
    this.items.push({
      order,
      text: '',
      type: 'text'
    });
  }

  hasMultipleItems() {
    return this.items.length > 1;
  }

  removeItem(itemToBeDeleted) {
    const index = this.items.indexOf(itemToBeDeleted)
    this.items.splice(index, 1);
    this.items.forEach((item, index) => item.order = index + 1);
  }
}
