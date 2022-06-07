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

from Common.init import Attribute, Source, pd, json, string, nltk, re
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize


def CheckEmpty(data):
    return data.strip() if data else None


def CheckNan(data, resultIfNan=None):
    return resultIfNan if pd.isnull(data) else data.strip()


def PrintStructure(source):
    for row in source:
        print(row)


def WriteStructureToFile(filePath, source):
    with open(filePath, "w") as file:
        for row in source:
            file.write(str(row) + "\n")


def WriteDictToJsonlFile(filePath, dictionary, keyName, valueName):
    with open(filePath, "w") as jsonlFile:
        for key, value in dictionary.items():
            jsonRow = {keyName: key, valueName: value}
            json.dump(jsonRow, jsonlFile)
            jsonlFile.write("\n")


def RemovePunctuation(text):
    stringPunctuation = string.punctuation
    return ''.join([c for c in text if c not in stringPunctuation])


def PreprocessingDiseaseName(diseaseName):
    # Replacing dash with space
    diseaseNameWithoutDash = diseaseName.replace('-', ' ')
    # Replacing slash with space
    diseaseNameWithoutSlash = diseaseNameWithoutDash.replace('/', ' ')
    # Remove multiple spaces
    diseaseNameWithoutMultipleSpaces = re.sub(' +', ' ', diseaseNameWithoutSlash)
    # Punctuation Removal
    diseaseNameWithoutPunctuation = RemovePunctuation(diseaseNameWithoutMultipleSpaces)
    # Lowering the text
    diseaseNameLower = diseaseNameWithoutPunctuation.lower()
    # Tokenization
    diseaseNameTokenized = word_tokenize(diseaseNameLower)
    # Removing Stopwords
    stopwords = nltk.corpus.stopwords.words("english")
    stopwords.remove("with")
    stopwords.remove("i")
    stopwords.append("type")
    diseaseNameWithoutStopwords = [word for word in diseaseNameTokenized if word not in stopwords]
    # Stemming
    porterStemmer = PorterStemmer()
    diseaseNameStemmed = [porterStemmer.stem(word) for word in diseaseNameWithoutStopwords]
    # Lemmatization
    wordnetLemmatizer = WordNetLemmatizer()
    diseaseNameLemmatized = [wordnetLemmatizer.lemmatize(word) for word in diseaseNameStemmed]

    return diseaseNameLemmatized


def JaccardSimilarity(doc1, doc2):
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


def GetAttribute(getMethods):
    for getMethod in getMethods:
        attribute = getMethod()
        if attribute is not None:
            return attribute

    return None
