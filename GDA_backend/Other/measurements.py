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

from GDA_backend.Common.constants import DOID_SOURCE_XREF_OMIM, DOID_SOURCE_XREF_UMLS, DOID_SOURCE_XREF_MESH, \
    DOID_SOURCE_XREF_GARD, DOID_SOURCE_XREF_MEDDRA, DOID_SOURCE_XREF_ICD10, DOID_SOURCE_SEARCH_ENGINE, \
    DOID_SOURCE_FROZEN_SET, DOID_SOURCE_DATABASE
from GDA_backend.Common.init import pd, tabulate, copy


def DoidAccuracy(annotationFilePath, doidAccuracyFilePath):
    annotationData = pd.read_csv(annotationFilePath, sep='\t', dtype=str)
    annotationData = annotationData[["Source", "DOID Source"]]
    annotationData = annotationData.groupby("Source", as_index=False).agg(list)
    annotationData = annotationData.to_numpy()

    XREF_100_KEY = 101
    FROZENSET_100_KEY = 102
    DATABASE_100_KEY = 103
    TYPESENSE_100_KEY = 104
    TOTAL_KEY = 105

    HEADER_SOURCE = ["", "OMIM", "UMLS", "MeSH", "GARD", "MedDRA", "ICD10", "Frozenset", "Typesense", "Database",
                     "None", "Total"]
    SOURCE_NUMBER = 12
    sourceMapping = {
        DOID_SOURCE_XREF_OMIM: 1,
        DOID_SOURCE_XREF_UMLS: 2,
        DOID_SOURCE_XREF_MESH: 3,
        DOID_SOURCE_XREF_GARD: 4,
        DOID_SOURCE_XREF_MEDDRA: 5,
        DOID_SOURCE_XREF_ICD10: 6,
        DOID_SOURCE_FROZEN_SET: 7,
        DOID_SOURCE_SEARCH_ENGINE: 8,
        DOID_SOURCE_DATABASE: 9,
        "None": 10,
        TOTAL_KEY: 11
    }

    HEADER_ACCURACY = ["", "0%", "(0, 25]", "(25, 50]", "(50, 75]", "(75, 99]", "100% (Xref)",
                       "100% (Frozenset)", "100% (Database)", "100% (Typesense)", "100% Total", "None", "Total"]

    accuracySource100Key = {
        DOID_SOURCE_XREF_OMIM: XREF_100_KEY,
        DOID_SOURCE_XREF_UMLS: XREF_100_KEY,
        DOID_SOURCE_XREF_MESH: XREF_100_KEY,
        DOID_SOURCE_XREF_GARD: XREF_100_KEY,
        DOID_SOURCE_XREF_MEDDRA: XREF_100_KEY,
        DOID_SOURCE_XREF_ICD10: XREF_100_KEY,
        DOID_SOURCE_FROZEN_SET: FROZENSET_100_KEY,
        DOID_SOURCE_SEARCH_ENGINE: TYPESENSE_100_KEY,
        DOID_SOURCE_DATABASE: DATABASE_100_KEY
    }

    ACCURACY_NUMBER = 13
    accuracyMapping = {
        # Accuracy count
        0: 1,  # Accuracy from 0 (minimum)
        25: 2,  # Accuracy from (0, 0.25]/(0, 25] -> %
        50: 3,  # Accuracy from (0.25, 0.50]/(25, 50] -> %
        75: 4,  # Accuracy from (0.50, 0.75]/(50, 75] -> %
        99: 5,  # Accuracy from (0.75, 0.99]/(75, 99] -> %
        XREF_100_KEY: 6,  # Accuracy 1/100% (maximum) Xref
        FROZENSET_100_KEY: 7,  # Accuracy 1/100% (maximum) Frozenset
        DATABASE_100_KEY: 8,  # Accuracy 1/100% (maximum) Database
        TYPESENSE_100_KEY: 9,  # Accuracy 1/100% (maximum) Typesense
        100: 10,  # Accuracy 1/100% (maximum)
        "None": 11,
        TOTAL_KEY: 12
    }

    tableSource = []
    tableAccuracy = []
    sourceTotalCount = [0] * SOURCE_NUMBER
    accuracyTotalCount = [0] * ACCURACY_NUMBER
    for row in annotationData:
        sourceName = row[0]
        doidSources = row[1]
        sourceCount = [0] * SOURCE_NUMBER
        accuracyCount = [0] * ACCURACY_NUMBER
        for doidSource in doidSources:
            if DOID_SOURCE_SEARCH_ENGINE in doidSource:
                sourceCount[sourceMapping[DOID_SOURCE_SEARCH_ENGINE]] += 1
                accuracy = int(doidSource.split(", ")[1][:-1])
                if accuracy == 0:
                    accuracyCount[accuracyMapping[0]] += 1
                elif 0 < accuracy <= 25:
                    accuracyCount[accuracyMapping[25]] += 1
                elif 25 < accuracy <= 50:
                    accuracyCount[accuracyMapping[50]] += 1
                elif 50 < accuracy <= 75:
                    accuracyCount[accuracyMapping[75]] += 1
                elif 75 < accuracy <= 99:
                    accuracyCount[accuracyMapping[25]] += 1
                elif accuracy == 100:
                    accuracyCount[accuracyMapping[100]] += 1
                    accuracyCount[accuracyMapping[TYPESENSE_100_KEY]] += 1
            elif doidSource == "None":
                sourceCount[sourceMapping[doidSource]] += 1
                accuracyCount[accuracyMapping[doidSource]] += 1
            else:
                sourceCount[sourceMapping[doidSource]] += 1
                accuracyCount[accuracyMapping[100]] += 1
                accuracyCount[accuracyMapping[accuracySource100Key[doidSource]]] += 1

        sourceCount[sourceMapping[TOTAL_KEY]] = sum(sourceCount)
        accuracyCount[accuracyMapping[TOTAL_KEY]] = sum(accuracyCount) - accuracyCount[accuracyMapping[100]]
        accuracyCount[0] = sourceCount[0] = sourceName

        for i in range(len(sourceCount) - 1):
            sourceTotalCount[i + 1] += sourceCount[i + 1]

        for i in range(len(accuracyCount) - 1):
            accuracyTotalCount[i + 1] += accuracyCount[i + 1]

        tableSource.append(sourceCount)
        tableAccuracy.append(accuracyCount)

    totalCount = sourceTotalCount[sourceMapping[TOTAL_KEY]]

    sourceTotalCountPercentage = [
        int(round((x / totalCount) * 100, 0)) if int(round((x / totalCount) * 100, 0)) >= 1 or x == 0 else
        round((x / totalCount) * 100, 3) for x in sourceTotalCount]
    accuracyTotalCountPercentage = [
        int(round((x / totalCount) * 100, 0)) if int(round((x / totalCount) * 100, 0)) >= 1 or x == 0 else
        round((x / totalCount) * 100, 3) for x in accuracyTotalCount]

    accuracyTotalCount[0] = sourceTotalCount[0] = "Total"
    tableSource.append(sourceTotalCount)
    tableAccuracy.append(accuracyTotalCount)
    accuracyTotalCountPercentage[0] = sourceTotalCountPercentage[0] = "Total %"
    tableSource.append(sourceTotalCountPercentage)
    tableAccuracy.append(accuracyTotalCountPercentage)

    # Creating accuracy percentage table
    tableAccuracyPercentage = copy.deepcopy(tableAccuracy)
    del tableAccuracyPercentage[len(tableAccuracyPercentage) - 2]
    for j in range(len(tableAccuracyPercentage) - 1):
        row = tableAccuracyPercentage[j]
        rowLen = len(row)
        for i in range(rowLen - 2):
            x = row[i + 1]
            rowCount = row[rowLen - 1]
            row[i + 1] = int(round((x / rowCount) * 100, 0)) if int(round((x / rowCount) * 100, 0)) >= 1 or x == 0 else \
                round((x / rowCount) * 100, 3)

    with open(doidAccuracyFilePath, "w") as file:
        file.write("Accuracy table\n\n")
        file.write(tabulate(tableAccuracy, HEADER_ACCURACY, tablefmt="pretty") + '\n\n')
        # Accuracy Table Percentage
        file.write("Accuracy percentage table\n\n")
        file.write(tabulate(tableAccuracyPercentage, HEADER_ACCURACY, tablefmt="pretty") + '\n\n')
        # Source Table
        file.write("Source table\n\n")
        file.write(tabulate(tableSource, HEADER_SOURCE, tablefmt="pretty") + '\n\n')
        file.write("Total number of rows: " + str(totalCount))
