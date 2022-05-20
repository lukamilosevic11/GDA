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

from Classes.annotation_row import UniprotRow
from Common.constants import UNIPROT_PATH


class Uniprot:
    @staticmethod
    def Read(filePath=UNIPROT_PATH):
        uniprotSet = set()
        with open(filePath, 'r') as uniprotFile:
            uniprotLines = uniprotFile.readlines()
            filteredLines = list(filter(lambda row: "Gene_Name" in row or "GeneID" in row or "UniProtKB-ID" in row
                                                    or "Gene_Synonym" in row or ("Ensembl" in row and "ENSG" in row),
                                        uniprotLines))
            filteredLines.append("x\tUniProtKB-ID\ty")  # Added to force parsing last UniProtKB-ID term

            currentUniprotID = None
            symbols = []
            symbolSynonymsDict = {}
            entrezIDs = []
            ensemblIDs = []
            for line in filteredLines:
                uniprotID = currentUniprotID
                currentUniprotID, valueType, value = map(str.strip, line.strip().split(maxsplit=2))
                if valueType == "UniProtKB-ID" and symbols:
                    if len(symbols) == 1 and len(entrezIDs) <= 1 and len(ensemblIDs) <= 1:
                        symbol = symbols[0]
                        symbolSynonyms = symbolSynonymsDict[symbol]
                        entrezID = entrezIDs[0] if entrezIDs else None
                        ensemblID = ensemblIDs[0] if ensemblIDs else None
                        uniprotSet.add(UniprotRow(symbol, symbolSynonyms, entrezID, ensemblID, uniprotID))
                    else:
                        for symbol in symbols:
                            symbolSynonyms = symbolSynonymsDict[symbol]
                            uniprotSet.add(UniprotRow(symbol, symbolSynonyms, None, None, uniprotID))
                    symbols = []
                    symbolSynonymsDict = {}
                    entrezIDs = []
                    ensemblIDs = []
                elif valueType == "Gene_Name":
                    symbols.append(value)
                    symbolSynonymsDict[value] = []
                elif valueType == "Gene_Synonym":
                    symbolSynonymsDict[symbols[-1]].append(value)
                elif valueType == "GeneID":
                    entrezIDs.append(value)
                elif valueType == "Ensembl":
                    ensemblIDs.append(value)

        return uniprotSet
