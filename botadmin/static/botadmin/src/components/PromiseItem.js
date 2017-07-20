import React from 'react';
import _ from 'lodash';
import { Button } from "react-bootstrap";

export default ({
                  addPromise,
                  promises_modal
                }) => ({
                         result
                       }) =>
  <li className="list-group-item">
    <span className="badge">
      {result._source.promisor_name},{' '}
      {result._source.parliament_period_name}
    </span>

    <span dangerouslySetInnerHTML={{
      __html: _.get(
        result,
        'highlight.body',
        result._source.body
      )
    }}
    />&nbsp;
    <Button bsSize="xsmall" onClick={() => addPromise(promises_modal.alternative_index, result._source, result._id)}>Legg til</Button>
  </li>;