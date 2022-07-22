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

from GDA_backend.Classes.annotation_models import HugoRow
from GDA_backend.Common.constants import HUGO_PATH
from GDA_backend.Common.init import pd, OrderedSet
from GDA_backend.Common.util import CheckNan


def ExtractValues(values):
    if not values:
        return None, []

    splittedValues = values.split("|")
    if len(splittedValues) > 1:
        return None, [CheckNan(splittedValue) for splittedValue in splittedValues]

    return CheckNan(splittedValues[0]), []


class Hugo:
    @staticmethod
    def Read(filePath=HUGO_PATH):
        hugoData = pd.read_csv(filePath, sep='\t', dtype=str)
        hugoData = hugoData[["symbol", "alias_symbol", "entrez_id", "uniprot_ids", "ensembl_gene_id"]]
        hugoData = hugoData.to_numpy()

        hugoSet = OrderedSet()
        for row in hugoData:
            symbol = CheckNan(row[0])
            aliasSymbols = CheckNan(row[1], [])
            if aliasSymbols:
                aliasSymbols = [CheckNan(aliasSymbol) for aliasSymbol in aliasSymbols.split("|")]

            entrezID = CheckNan(row[2])
            uniprotID, uniprotIDs = ExtractValues(CheckNan(row[3], []))
            ensemblID = CheckNan(row[4])
            hugoSet.add(HugoRow(symbol, entrezID, uniprotID, ensemblID, uniprotIDs, aliasSymbols))

        return hugoSet
