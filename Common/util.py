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
from Common.init import Attribute, Source, PD, json, string, nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


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


def writeDictToJsonlFile(filePath, dictionary, keyName, valueName):
    with open(filePath, "w") as jsonlFile:
        for key, value in dictionary.items():
            jsonRow = {keyName: key, valueName: value}
            json.dump(jsonRow, jsonlFile)
            jsonlFile.write("\n")


def removePunctuation(text):
    stringPunctuation = string.punctuation
    return ''.join([c for c in text if c not in stringPunctuation])


def preprocessingDiseaseName(diseaseName):
    # Replacing dash with space
    diseaseNameWithoutDash = diseaseName.replace('-', ' ')
    # Replacing slash with space
    diseaseNameWithoutSlash = diseaseNameWithoutDash.replace('/', ' ')
    # Punctuation Removal
    diseaseNameWithoutPunctuation = removePunctuation(diseaseNameWithoutSlash)
    # Lowering the text
    diseaseNameLower = diseaseNameWithoutPunctuation.lower()
    # Tokenization
    diseaseNameTokenized = word_tokenize(diseaseNameLower)
    # Removing Stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    diseaseNameWithoutStopwords = [word for word in diseaseNameTokenized if word not in stopwords]
    # Stemming
    porterStemmer = PorterStemmer()
    diseaseNameStemmed = [porterStemmer.stem(word) for word in diseaseNameWithoutStopwords]
    # Lemmatization
    wordnetLemmatizer = WordNetLemmatizer()
    diseaseNameLemmatized = [wordnetLemmatizer.lemmatize(word) for word in diseaseNameStemmed]

    return diseaseNameLemmatized


def jaccardSimilarity(doc1, doc2):
    # List the unique words in a document
    wordsDoc1 = set(doc1.split())
    wordsDoc2 = set(doc2.split())

    # Find the intersection of words list of doc1 & doc2
    intersection = wordsDoc1.intersection(wordsDoc2)

    # Find the union of words list of doc1 & doc2
    union = wordsDoc1.union(wordsDoc2)

    # Calculate Jaccard similarity score
    # using length of intersection set divided by length of union set
    return float(len(intersection)) / len(union)
