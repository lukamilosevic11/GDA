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

from GDA_backend.Common.constants import API_KEY
from GDA_backend.Common.init import typesense


class SearchEngineClient:
    def __init__(self, hostName, apiKey=API_KEY, nodes=None, connectionTimeoutSeconds=10):
        if nodes is None:
            # "host" variable should be changed based on way of execution:
            # docker (name of container for typesense)
            # independent app(localhost)
            nodes = [{"host": hostName, "port": "8108", "protocol": "http"}]
        elif "host" not in nodes[0]:
            nodes[0]["host"] = hostName

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

    def GetAllCollectionNames(self):
        return self.client.collections.retrieve()

    def ImportDataFromFile(self, name, filePath, batchSize=200):
        result = None
        with open(filePath, "r") as jsonlFile:
            result = self.client.collections[name].documents.import_(jsonlFile.read().encode("utf-8"),
                                                                     {"batch_size": batchSize})

        return result

    def SearchByQuery(self, name, query, queryBy, sortBy="_text_match:desc"):
        searchParameters = {
            "q": query,
            "query_by": queryBy,
            "sort_by": sortBy,
            "num_typos": 0
        }

        return self.client.collections[name].documents.search(searchParameters)
