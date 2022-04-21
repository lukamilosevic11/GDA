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

from Classes import annotationrow as ar
from Common import init, util


class Hugo:
    @staticmethod
    def Read(filePath):
        hugoData = init.PD.read_csv(filePath, sep='\t', dtype=str)
        hugoData = hugoData[["symbol", "entrez_id", "uniprot_ids", "ensembl_gene_id"]]
        hugoData = hugoData.to_numpy()

        hugoSet = set()
        for row in hugoData:
            symbol = util.checkNan(row[0])
            entrezID = util.checkNan(row[1])
            uniprotIDs = util.checkNan(row[2], [])
            ensemblID = util.checkNan(row[3])
            hugoSet.add(ar.HugoRow(symbol, entrezID, ensemblID, uniprotIDs))

        return hugoSet
