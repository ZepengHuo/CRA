import copy

class QueryIterate:
    """"
    Helps with iteration in TozStore queries. The resulting iterator
    can only be consumed once.
    If the list will fit in memory, you can copy the results into a list.
    For example

    list_of_records = list(QueryIterate(client, query))

    For larger queries, you can create a new QueryIterator for each
    traversal.
    """

    def __init__(self, client, query, next_token=0, max=-1):
        self.first_query = True
        self.position = next_token
        self.client = client
        self.query = copy.deepcopy(query)
        self.has_data = False
        self.max = max
        self.total_count = 0
        # Perform first query
        self.results = self.client.search(self.query)
        self.total_results = self.results.total_results
        self.has_data = self.total_results > 0
        self.result_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if (self.max > 0 and self.total_count >= self.max):
            raise StopIteration
        if self.has_data == False:
            raise StopIteration
        # Check if we have any results to iterate through
        if self.result_index < len(self.results):
            retval = self.results.records[self.result_index]
            self.result_index += 1
            self.total_count += 1
            return retval
        elif self.results.next_token > 0:  # We have to do another query to get more results
            self.query.next_token = self.results.next_token
            self.results = self.client.search(self.query)
            self.result_index = 0
            if len(self.results) > 0:
                retval = self.results.records[self.result_index]
                self.result_index += 1
                self.total_count += 1
                return retval
        else:  # out of results and out of further queries
            raise StopIteration

    def __len__(self):
        return self.total_results

    def raiseIfNone(self, msg="No records found. Please check your query and verify you are authorized for the requested data."):
        if self.has_data == False:
            raise RuntimeError(msg)
