import * as React from "react";
import { Button, Modal } from "react-bootstrap";
import {
  ActionBar, ActionBarRow, Hits, HitsStats,
  Layout, LayoutBody, LayoutResults, NoHits, PaginationSelect, RefinementListFilter, SearchBox, SearchkitManager,
  SearchkitProvider,
  SelectedFilters, SideBar,
  TopBar
} from "searchkit";
import Pagination from "react-bootstrap/es/Pagination";
import { translations } from '../utils/translations';
import { customHighlight } from "../utils/customHighlight";
import PromiseItem from "./PromiseItem";

const searchkit = new SearchkitManager(
  'https://search.holderdeord.no/hdo_production_promises/'
);

searchkit.translateFunction = key => translations[ key ];

searchkit.setQueryProcessor(query => {
  if (!query.query) {
    // empty query! sort by period name descending
    query.sort = { parliament_period_name: { order: 'desc' } };
  }

  return query;
});

const PromisesModal = ({
                         closePromisesModal,
                         promises_modal
                       }) => (
  <Modal bsSize="large"
         show={promises_modal.open}
         onHide={closePromisesModal}>
    <Modal.Header closeButton>
      <Modal.Title>Løfter</Modal.Title>
    </Modal.Header>
    <Modal.Body>
      <SearchkitProvider searchkit={searchkit}>
        <Layout>
          <TopBar>
            <SearchBox
              autofocus
              searchOnChange
              prefixQueryFields={[ 'body' ]}
            />
          </TopBar>
          <LayoutBody className="row">
            <SideBar className="col-md-4">
              <RefinementListFilter
                id="period"
                title="Stortingsperiode"
                field="parliament_period_name"
                size={10}
                orderKey="_term"
              />

              <RefinementListFilter
                id="parties"
                title="Partier og regjeringer"
                field="promisor_name"
                size={10}
                operator="OR"
                orderKey="_term"
              />

              <RefinementListFilter
                id="categories"
                title="Kategorier"
                field="category_names"
                size={10}
              />
            </SideBar>

            <LayoutResults className="col-md-8">
              <ActionBar>
                <ActionBarRow>
                  <HitsStats />
                  <SelectedFilters />
                </ActionBarRow>
              </ActionBar>

              <Hits
                hitsPerPage={30}
                highlightFields={[ 'body' ]}
                customHighlight={customHighlight}
                itemComponent={PromiseItem}
              />

              <NoHits suggestionsField="body"/>

              <Pagination/>

              <PaginationSelect />

            </LayoutResults>
          </LayoutBody>
        </Layout>
      </SearchkitProvider>
    </Modal.Body>
    <Modal.Footer>
      <Button onClick={closePromisesModal}>Close</Button>
    </Modal.Footer>
  </Modal>
);

export default PromisesModal;
