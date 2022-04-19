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
from Common import init


# TODO: fix read method parsing doesn't work properly
class Uniprot:
    @staticmethod
    def Read(filePath):
        uniprotSet = set()
        with open(filePath, 'r') as uniprotFile:
            uniprotLines = uniprotFile.readlines()
            filteredLines = list(filter(lambda row: "Gene_Name" in row or "GeneID" in row or "UniProtKB-ID" in row or
                                                    ("Ensembl" in row and "ENSG" in row), uniprotLines))
            symbol = None
            entrezID = None
            ensemblID = None
            uniprotID = None
            currentUniprotID = None
            for line in filteredLines:
                uniprotID = currentUniprotID
                currentUniprotID, valueType, value = line.strip().split(maxsplit=2)
                if valueType == "UniProtKB-ID" and (symbol is not None or entrezID is not None
                                                    or ensemblID is not None):
                    uniprotSet.add(ar.UniprotRow(symbol, entrezID, uniprotID))
                    symbol = None
                    entrezID = None
                elif valueType == "Gene_Name":
                    symbol = value
                elif valueType == "GeneID":
                    entrezID = value

        return uniprotSet
