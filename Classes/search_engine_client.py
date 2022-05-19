from Common.init import typesense, json
from Common.constants import API_KEY


class SearchEngineClient:
    def __init__(self, apiKey=API_KEY, nodes=None, connectionTimeoutSeconds=2):
        if nodes is None:
            nodes = [{"host": "localhost", "port": "8108", "protocol": "http"}]

        self.client = typesense.Client({
            "api_key": apiKey,
            "nodes": nodes,
            "connection_timeout_seconds": connectionTimeoutSeconds
        })

    def createCollection(self, name, fields):
        return self.client.collections.create({
            "name": name,
            "fields": fields
        })

    def deleteCollection(self, name):
        return self.client.collections[name].delete()

    def getAllCollections(self):
        return self.client.collections.retrieve()

    def importDataFromFile(self, name, filePath, batchSize=200):
        result = None
        with open(filePath, "r") as jsonlFile:
            result = self.client.collections[name]. \
                documents.import_(jsonlFile.read().encode("utf-8"), {"batch_size": batchSize})

        return result

    def searchByQuery(self, name, query, queryBy, sortBy="_text_match:desc"):
        searchParameters = {
            "q": query,
            "query_by": queryBy,
            "sort_by": sortBy
        }

        return self.client.collections[name].documents.search(searchParameters)

    @staticmethod
    def searchResultToString(searchResult):
        res = ""
        if len(searchResult["hits"]) > 0:
            res += "*************************************************************************************************\n"
            res += json.dumps(searchResult["hits"][0]["document"], indent=2, sort_keys=True)
            res += "*************************************************************************************************"

        return res
