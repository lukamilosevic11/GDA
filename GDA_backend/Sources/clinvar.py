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

from GDA_backend.Classes.annotation_row import ClinVarRow
from GDA_backend.Common.constants import CLINVAR_PATH
from GDA_backend.Common.init import pd, OrderedSet
from GDA_backend.Common.util import CheckNan


class ClinVar:
    @staticmethod
    def Read(filePath=CLINVAR_PATH):
        clinVarData = pd.read_csv(filePath, sep='\t', dtype=str)
        clinVarData = clinVarData[["#GeneID", "AssociatedGenes", "RelatedGenes", "ConceptID", "DiseaseName",
                                   "DiseaseMIM"]]
        clinVarData = clinVarData.to_numpy()

        clinVarSet = OrderedSet()
        for row in clinVarData:
            associatedGeneSymbol = CheckNan(row[1])
            relatedGeneSymbol = CheckNan(row[2])
            entrezID = CheckNan(row[0])
            diseaseName = CheckNan(row[4])
            umls = CheckNan(row[3])
            omim = CheckNan(row[5])
            if associatedGeneSymbol is not None:
                clinVarSet.add(ClinVarRow(associatedGeneSymbol, entrezID, diseaseName, umls, omim))

            if relatedGeneSymbol is not None:
                clinVarSet.add(ClinVarRow(relatedGeneSymbol, entrezID, diseaseName, umls, omim))

        return clinVarSet
