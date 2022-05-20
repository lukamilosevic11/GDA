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

from Classes.annotation_row import ClinVarRow
from Common.constants import CLINVAR_PATH
from Common.init import PD
from Common.util import CheckNan


class ClinVar:
    @staticmethod
    def Read(filePath=CLINVAR_PATH):
        clinVarData = PD.read_csv(filePath, sep='\t', dtype=str)
        clinVarData = clinVarData[["#GeneID", "AssociatedGenes", "RelatedGenes", "DiseaseName"]]
        clinVarData = clinVarData.to_numpy()

        clinVarSet = set()
        for row in clinVarData:
            associatedGeneSymbol = CheckNan(row[1])
            relatedGeneSymbol = CheckNan(row[2])
            entrezID = CheckNan(row[0])
            diseaseName = CheckNan(row[3])
            if associatedGeneSymbol is not None:
                symbol = associatedGeneSymbol
            else:
                symbol = relatedGeneSymbol
            clinVarSet.add(ClinVarRow(symbol, entrezID, diseaseName))
        return clinVarSet
