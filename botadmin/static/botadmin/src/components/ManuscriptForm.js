import React from 'react';

const ManuscriptTypeEnum = {
  Info: 'info',
  ElectoralGuide: 'electoralGuide'
};

class ManuscriptForm extends React.Component {
  // state = {
  //   manuscript: new CoreManuscript()
  // };
  types = [
    { pk: 1, name: 'Info', type: ManuscriptTypeEnum.Info },
    { pk: 2, name: 'ElectoralGuide', type: ManuscriptTypeEnum.ElectoralGuide }
  ];

  // componentDidMount() {
  //   console.log('mounting', this.props.manuscript);
  //   this.setState({
  //     manuscript: this.props.manuscript
  //   });
  // }

  // handleManuscriptNameChange(event) {
  //   this.props.manuscript.name = event.target.value;
  //   this.forceUpdate();
  // }
  //
  // handleManuscriptTypeChange(event) {
  //   this.props.manuscript.type = event.target.value;
  //   this.forceUpdate();
  // }

  addManuscriptItem() {
    this.props.manuscript.addItem();
    this.forceUpdate();
  }

  handleManuscriptPropertyChange(event, propertyName) {
    this.props.manuscript[ propertyName ] = event.target.value;
    this.forceUpdate();
  }

  handleFormSubmit(event) {
    event.preventDefault();
    this.props.handleSubmit(event);
  }

  handleEventPropertyChange(event, item, propertyName) {
    item[ propertyName ] = event.target.value;
    this.forceUpdate();
  }

  render() {
    console.log('ManuscriptForm.render', this.props.manuscript);
    return (
      <div className="row">
        <div className="col-md-6">
          <form onSubmit={event => this.handleFormSubmit(event)}>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input className="form-control" type="text" id="name" name="name"
                     onChange={event => this.handleManuscriptPropertyChange(event, 'name')}
                     value={this.props.manuscript.name}/>
            </div>
            <div className="form-group">
              <label htmlFor="type">Category</label>
              <select className="form-control" id="type" name="type"
                      onChange={event => this.handleManuscriptPropertyChange(event, 'type')}
                      value={this.props.manuscript.type}>
                { this.types.map(this.renderCategoryOption) }
              </select>
            </div>
            <div className="well">
              {this.props.manuscript.items.map((item, index) => this.renderManuscriptItem(item, index))}
              <button className="btn btn-link" type="button"
                      onClick={event => this.addManuscriptItem(event)}>Add item</button>
            </div>
            <button type="submit" className="btn btn-default">Submit</button>
          </form>
        </div>
        <div className="col-md-6">Preview</div>
      </div>
    );
  }

  renderCategoryOption({ pk, name, type }) {
    return (
      <option key={pk} value={type}>{name}</option>
    );
  }

  renderManuscriptItem(item, index) {
    let { order, text, type } = item;
    return (
      <div key={order} className="panel panel-default">
        <div className="panel-heading">Item #{order}</div>
        <div className="panel-body">
          <div className="form-group">
            <label htmlFor={`itemType-${order}`}>Type</label>
            <select className="form-control" id={`itemType-${order}`} name="itemType"
                    onChange={event => this.handleEventPropertyChange(event, item, 'type')}
                    value={type}>
              <option value="text">Text</option>
              <option value="button">Button</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor={`itemText-${order}`}>Text</label>
            <input className="form-control" type="text" id={`itemText-${order}`} name="itemText"
                   onChange={event => this.handleEventPropertyChange(event, item, 'text')}
                   defaultValue={text}/>
          </div>
        </div>
      </div>
    );
  }
}

export default ManuscriptForm;
