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
from Common import init, util


class ClinVar:
    @staticmethod
    def Read(filePath):
        clinVarData = init.PD.read_csv(filePath, sep='\t', dtype=str)
        clinVarData = clinVarData[["#GeneID", "AssociatedGenes", "RelatedGenes", "DiseaseName"]]
        clinVarData = clinVarData.to_numpy()

        clinVarSet = set()
        for row in clinVarData:
            associatedGeneSymbol = row[1]
            relatedGeneSymbol = row[2]
            entrezID = row[0].strip()
            diseaseName = row[3].strip()
            if not init.PD.isnull(associatedGeneSymbol):
                symbol = associatedGeneSymbol.strip()
            else:
                symbol = relatedGeneSymbol.strip()
            clinVarSet.add(ar.ClinVarRow(symbol, entrezID, diseaseName))
        return clinVarSet
