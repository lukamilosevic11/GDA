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

from GDA_backend.Classes.annotation_row import EnsemblRow
from GDA_backend.Common.constants import ENSEMBL_ENTREZ_PATH, ENSEMBL_UNIPROT_PATH
from GDA_backend.Common.init import pd, OrderedSet
from GDA_backend.Common.util import CheckNan


def CheckEmptyEnsembl(value):
    return value if value is not None and value != "-" else None


class Ensembl:
    @staticmethod
    def Read(filePathEntrez=ENSEMBL_ENTREZ_PATH, filePathUniprot=ENSEMBL_UNIPROT_PATH):
        filePaths = [filePathEntrez, filePathUniprot]
        ensemblSet = OrderedSet()
        for filePath in filePaths:
            ensemblData = pd.read_csv(filePath, sep='\t', dtype=str)
            ensemblData = ensemblData[["gene_stable_id", "protein_stable_id", "xref"]]
            ensemblData = ensemblData.sort_values("protein_stable_id", ascending=False)
            ensemblData = ensemblData.to_numpy()

            for row in ensemblData:
                ensemblID = CheckEmptyEnsembl(CheckNan(row[0]))
                ensemblProteinID = CheckEmptyEnsembl(CheckNan(row[1]))
                if filePath == ENSEMBL_ENTREZ_PATH:
                    entrezID = CheckEmptyEnsembl(CheckNan(row[2]))
                    ensemblSet.add(EnsemblRow(entrezID, None, ensemblID, ensemblProteinID))
                elif filePath == ENSEMBL_UNIPROT_PATH:
                    uniprotID = CheckEmptyEnsembl(CheckNan(row[2]))
                    ensemblSet.add(EnsemblRow(None, uniprotID, ensemblID, ensemblProteinID))

        return ensemblSet
