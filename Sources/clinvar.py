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
from common import init, util


class ClinVar:
    @staticmethod
    def Read(filePath):
        clinVarData = init.PD.read_csv(filePath, sep='\t')
        clinVarData = clinVarData[["#GeneID", "AssociatedGenes", "RelatedGenes", "DiseaseName"]]
        clinVarData = clinVarData.to_numpy()

        clinVarSet = set()
        for row in clinVarData:
            associatedGeneSymbol = str(row[1]).strip()
            relatedGeneSymbol = str(row[2]).strip()
            entrezID = str(row[0]).strip()
            diseaseName = str(row[3]).strip()
            symbol = None
            if not util.isNan(associatedGeneSymbol):
                symbol = associatedGeneSymbol
            else:
                symbol = relatedGeneSymbol
            clinVarSet.add(ar.ClinVarRow(symbol, entrezID, diseaseName))
        return clinVarSet
