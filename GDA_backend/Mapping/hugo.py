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

from GDA_backend.Classes.annotation_row import HugoRow
from GDA_backend.Common.constants import HUGO_PATH
from GDA_backend.Common.init import pd, OrderedSet
from GDA_backend.Common.util import CheckNan


class Hugo:
    @staticmethod
    def Read(filePath=HUGO_PATH):
        hugoData = pd.read_csv(filePath, sep='\t', dtype=str)
        hugoData = hugoData[["symbol", "entrez_id", "uniprot_ids", "ensembl_gene_id"]]
        hugoData = hugoData.to_numpy()

        hugoSet = OrderedSet()
        for row in hugoData:
            symbol = CheckNan(row[0])
            entrezID = CheckNan(row[1])
            uniprotIDs = CheckNan(row[2], [])
            uniprotID = None
            if uniprotIDs:
                splittedUnirotIDs = uniprotIDs.split("|")
                if len(splittedUnirotIDs) > 1:
                    uniprotIDs = splittedUnirotIDs
                else:
                    uniprotID = splittedUnirotIDs[0].strip()
                    uniprotIDs = []
            ensemblID = CheckNan(row[3])
            hugoSet.add(HugoRow(symbol, entrezID, uniprotID, ensemblID, uniprotIDs))

        return hugoSet
