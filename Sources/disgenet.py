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

from Classes.annotation_row import DisGeNetRow
from Common.constants import DISGENET_PATH
from Common.init import PD
from Common.util import CheckNan


class DisGeNet:
    @staticmethod
    def Read(filePath=DISGENET_PATH):
        disGeNetData = PD.read_csv(filePath, sep='\t', dtype=str)
        disGeNetData = disGeNetData[["geneId", "geneSymbol", "diseaseId", "diseaseName"]]
        disGeNetData = disGeNetData.to_numpy()

        disGeNetSet = set()
        for row in disGeNetData:
            symbol = CheckNan(row[1])
            entrezID = CheckNan(row[0])
            umls = CheckNan(row[2])
            diseaseName = CheckNan(row[3])
            disGeNetSet.add(DisGeNetRow(symbol, entrezID, diseaseName, umls))

        return disGeNetSet
