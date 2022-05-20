#  GDA Copyright (c) 2022.
#  University of Belgrade, Faculty of Mathematics
#  Luka Milosevic
#  lukamilosevic11@gmail.com
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

from Common.constants import API_KEY
from Common.init import typesense, json


class SearchEngineClient:
    def __init__(self, apiKey=API_KEY, nodes=None, connectionTimeoutSeconds=2):
        if nodes is None:
            nodes = [{"host": "localhost", "port": "8108", "protocol": "http"}]

        self.client = typesense.Client({
            "api_key": apiKey,
            "nodes": nodes,
            "connection_timeout_seconds": connectionTimeoutSeconds
        })

    def CreateCollection(self, name, fields):
        return self.client.collections.create({
            "name": name,
            "fields": fields
        })

    def DeleteCollection(self, name):
        return self.client.collections[name].delete()

    def GetAllCollections(self):
        return self.client.collections.retrieve()

    def ImportDataFromFile(self, name, filePath, batchSize=200):
        result = None
        with open(filePath, "r") as jsonlFile:
            result = self.client.collections[name]. \
                documents.import_(jsonlFile.read().encode("utf-8"), {"batch_size": batchSize})

        return result

    def SearchByQuery(self, name, query, queryBy, sortBy="_text_match:desc"):
        searchParameters = {
            "q": query,
            "query_by": queryBy,
            "sort_by": sortBy
        }

        return self.client.collections[name].documents.search(searchParameters)

    @staticmethod
    def SearchResultToString(searchResult):
        res = ""
        if len(searchResult["hits"]) > 0:
            res += "*************************************************************************************************\n"
            res += json.dumps(searchResult["hits"][0]["document"], indent=2, sort_keys=True)
            res += "*************************************************************************************************"

        return res
