#  GDA Copyright (c) 2021.
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
import json
from Common.init import Attribute, Source, PD


def checkNan(data, resultIfNan=None):
    return resultIfNan if PD.isnull(data) else data.strip()


def printSet(sourceSet):
    for row in sourceSet:
        print(row)


def writeSetToFile(filePath, sourceSet):
    with open(filePath, "w") as file:
        for row in sourceSet:
            file.write(str(row) + "\n")


def setToJson(filePath, sourceSet, attributes, source):
    jsonArray = []
    for row in sourceSet:
        jsonRow = {}
        for attr in attributes:
            if attr == Attribute.SYMBOL:
                jsonRow["symbol"] = row.symbol
            elif attr == Attribute.ENTREZ_ID:
                jsonRow["entrezID"] = row.entrezID
            elif attr == Attribute.UNIPROT_ID:
                jsonRow["uniprotID"] = row.uniprotID
            elif attr == Attribute.ENSEMBL_ID:
                jsonRow["ensemblID"] = row.ensemblID
            elif attr == Attribute.DOID:
                jsonRow["doid"] = row.doid
            elif attr == Attribute.SOURCE:
                jsonRow["source"] = row.source
            elif attr == Attribute.DISEASE_NAME:
                jsonRow["diseaseName"] = row.diseaseName

        if source == Source.OBO:
            for synonym in row.getSynonyms():
                jsonOboRow = {"doid": row.doid, "diseaseName": synonym}
                jsonArray.append(jsonOboRow)

        jsonArray.append(jsonRow)

    return jsonArray


def writeJsonSetToFile(filePath, sourceSet, attributes, source):
    jsonSet = setToJson(filePath, sourceSet, attributes, source)
    with open(filePath, "w") as jsonFile:
        for jsonRow in jsonSet:
            json.dump(jsonRow, jsonFile)
            jsonFile.write("\n")
