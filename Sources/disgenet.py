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

from Classes import annotationrow as ar
from common import init


class DisGeNet:
    @staticmethod
    def Read(filePath):
        disGeNetData = init.PD.read_csv(filePath, sep='\t')
        disGeNetData = disGeNetData[["geneId", "geneSymbol", "diseaseId", "diseaseName"]]
        disGeNetData = disGeNetData.to_numpy()

        disGeNetSet = set()
        for row in disGeNetData:
            symbol = str(row[1]).strip()
            entrezID = str(row[0]).strip()
            umls = str(row[2]).strip()
            diseaseName = str(row[3]).strip()
            disGeNetSet.add(ar.DisGeNetRow(symbol, entrezID, diseaseName, umls))

        return disGeNetSet
