import React from 'react';
import { Button, ButtonGroup } from "react-bootstrap";

const ManuscriptAlternativeForm = ({
                                     alternative,
                                     changeManuscriptAlternativeProperty,
                                     deleteManuscriptAlternative,
                                     index,
                                     openPromisesModal,
                                     removePromiseFromAlternative
                                   }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        {index + 1}. {alternative.text}
      </div>
      <div className="panel-body">
        <div className="form-group">
          <label>Text</label>
          <input className="form-control"
                 onSelect={(event) => changeManuscriptAlternativeProperty(event, index, 'text')}
                 defaultValue={alternative.text}/>
        </div>
        <div className="form-group">
          <label>Promises</label>
          <ul>
            {alternative.full_promises.map(promise => (
              <li key={`alternative-promise-${index}-${promise.pk}`}>
                {promise.body}
                {' '}
                ({promise.promisor_name})
                {' '}
                <Button bsSize="xsmall" onClick={() => removePromiseFromAlternative(index, promise)}>
                  Remove
                </Button>
              </li>
            ))}
          </ul>
          <Button bsSize="small"
                  onClick={() => openPromisesModal(index)}>
            Add promise
          </Button>
        </div>
        <div className="form-group">
          <label>Parties</label>
          <p>{[ ...new Set(alternative.parties) ].join(', ')}</p>
        </div>
      </div>
      <div className="panel-footer clearfix">
        <ButtonGroup bsSize="xsmall" className="pull-right">
          <Button bsStyle="danger" onClick={() => deleteManuscriptAlternative(index)}>
            <span className="glyphicon glyphicon-remove"/> Remove
          </Button>
        </ButtonGroup>
      </div>
    </div>
  );
};

export default ManuscriptAlternativeForm;