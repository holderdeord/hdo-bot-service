import React from 'react';
import { Button } from "react-bootstrap";

const ManuscriptAlternativeForm = ({
                                     alternative,
                                     changeManuscriptAlternativeProperty,
                                     index,
                                     openPromisesModal,
                                     removePromiseFromAlternative
                                   }) => {
  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        {alternative.text}
      </div>
      <div className="panel-body">
        <div className="form-group">
          <label>Tekst</label>
          <input className="form-control"
                 onSelect={(event) => changeManuscriptAlternativeProperty(event, index, 'text')}
                 defaultValue={alternative.text}/>
        </div>
        <div className="form-group">
          <label>Løfter</label>
          <ul>
            {alternative.full_promises.map(promise => (
              <li key={`alternative-promise-${index}-${promise.pk}`}>
                {promise.body}
                {' '}
                ({promise.promisor_name})
                {' '}
                <Button bsSize="xsmall" onClick={() => removePromiseFromAlternative(index, promise)}>Fjern løfte</Button>
              </li>
            ))}
          </ul>
          <Button onClick={() => openPromisesModal(index)}>Legg til løfte</Button>
        </div>
        <div className="form-group">
          <label>Partier</label>
          <p>{[ ...new Set(alternative.parties) ].join(', ')}</p>
        </div>
      </div>
    </div>
  );
};

export default ManuscriptAlternativeForm;