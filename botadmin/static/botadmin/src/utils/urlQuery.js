import * as query_string from "query-string";

export const urlQuery = query_string.parse(window.location.search);
