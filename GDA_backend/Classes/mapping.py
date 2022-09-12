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

from GDA_backend.Classes.annotation_models import EnsemblRow, HugoRow, OBORow, OrphanetXrefRow, UniProtRow
from GDA_backend.Common.constants import ENSEMBL_ENTREZ_PATH, ENSEMBL_UNIPROT_PATH, HUGO_PATH, OBO_PATH, RGD_OBO_PATH, \
    ORPHANET_XREF_PATH, UNIPROT_PATH
from GDA_backend.Common.init import pd, et, OrderedSet, OrderedDict, Ontology, multiprocessing, Xref
from GDA_backend.Common.util import CheckNan, CheckEmpty


def CheckEmptyEnsembl(value):
    return value if value is not None and value != "-" else None


def ExtractValues(values):
    if not values:
        return None, []

    splittedValues = values.split("|")
    if len(splittedValues) > 1:
        return None, [CheckNan(splittedValue) for splittedValue in splittedValues]

    return CheckNan(splittedValues[0]), []


class MappingInput:
    @staticmethod
    def ReadEnsembl(filePathEntrez=ENSEMBL_ENTREZ_PATH, filePathUniprot=ENSEMBL_UNIPROT_PATH):
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

    @staticmethod
    def ReadHUGO(filePath=HUGO_PATH):
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

    @staticmethod
    def ReadOBO(returnObsoleteDOIDs=False, filePathOBO=OBO_PATH, filePathRGD=RGD_OBO_PATH):
        filePaths = [filePathRGD, filePathOBO]
        oboSet = OrderedSet()
        obsoleteSet = OrderedSet()

        for filePath in filePaths:
            oboData = Ontology(filePath, threads=multiprocessing.cpu_count())
            for term in oboData.terms():
                if term.obsolete:
                    doid = CheckEmpty(term.id)
                    if doid is not None:
                        obsoleteSet.add(doid)
                    continue

                doid = CheckEmpty(term.id)
                diseaseName = CheckEmpty(term.name)
                definition = CheckEmpty(term.definition)
                synonyms = term.synonyms
                parentDoids = list(term.superclasses(distance=1, with_self=False).to_set())
                xrefs = term.xrefs
                altIds = term.alternate_ids
                oboSet.add(OBORow(doid, diseaseName, synonyms, parentDoids, xrefs, altIds, definition))

        return (oboSet, obsoleteSet) if returnObsoleteDOIDs else oboSet

    @staticmethod
    def ReadOrphanetXref(filePath=ORPHANET_XREF_PATH):
        orphanetXrefSet = OrderedSet()
        tree = et.parse(filePath)
        root = tree.getroot()
        disorderList = root.find("DisorderList")
        for disorder in disorderList:
            disorderType = disorder.find("DisorderType").find("Name").text.strip()
            if disorderType != "Disease":
                continue

            skipDisorder = False
            disorderFlagList = disorder.find("DisorderFlagList")
            for disorderFlag in disorderFlagList:
                label = disorderFlag.find("Label").text
                if label is not None and label.strip() != "Head of classification":
                    skipDisorder = True

            if skipDisorder:
                continue

            orpha = disorder.find("OrphaCode").text.strip()
            diseaseName = disorder.find("Name").text.strip()
            eDict = {}
            btntDict = {}
            ntbtDict = {}
            otherDict = {}

            def addValueToMappingRelationDict(xref, valueP, mappingRelationP):
                if mappingRelationP == 'E':
                    if xref not in eDict:
                        eDict[xref] = set()
                    eDict[xref].add(valueP)
                elif mappingRelationP == "BTNT":
                    if xref not in btntDict:
                        btntDict[xref] = set()
                    btntDict[xref].add(valueP)
                elif mappingRelationP == "NTBT":
                    if xref not in ntbtDict:
                        ntbtDict[xref] = set()
                    ntbtDict[xref].add(valueP)
                else:
                    if xref not in otherDict:
                        otherDict[xref] = set()
                    otherDict[xref].add(valueP)

            externalReferenceList = disorder.find("ExternalReferenceList")
            for externalReference in externalReferenceList:
                source = externalReference.find("Source").text.strip()
                value = externalReference.find("Reference").text.strip()
                mappingRelation = externalReference.find("DisorderMappingRelation").find("Name").text.strip().split()[0]

                if source == "OMIM":
                    addValueToMappingRelationDict(Xref.OMIM, value, mappingRelation)
                elif source == "UMLS":
                    addValueToMappingRelationDict(Xref.UMLS, value, mappingRelation)
                elif source == "MeSH":
                    addValueToMappingRelationDict(Xref.MeSH, value, mappingRelation)
                elif source == "GARD":
                    addValueToMappingRelationDict(Xref.GARD, value, mappingRelation)
                elif source == "MedDRA":
                    addValueToMappingRelationDict(Xref.MedDRA, value, mappingRelation)
                elif source == "ICD-10":
                    addValueToMappingRelationDict(Xref.ICD10, value, mappingRelation)

            eDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), eDict.items())))
            btntDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), btntDict.items())))
            ntbtDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), ntbtDict.items())))
            otherDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), otherDict.items())))

            orphanetXrefSet.add(OrphanetXrefRow(orpha, eDict, btntDict, ntbtDict, otherDict, diseaseName))

        return orphanetXrefSet

    @staticmethod
    def ReadUniProt(filePath=UNIPROT_PATH):
        uniprotSet = OrderedSet()
        with open(filePath, 'r') as uniprotFile:
            uniprotLines = uniprotFile.readlines()
            filteredLines = list(filter(lambda row: "Gene_Name" in row or "GeneID" in row or "UniProtKB-ID" in row
                                                    or "STRING" in row or "Gene_Synonym" in row
                                                    or ("Ensembl" in row and "ENSG" in row), uniprotLines))
            filteredLines.append("x\tUniProtKB-ID\ty")  # Added to force parsing last UniProtKB-ID term

            currentUniprotID = None
            ensemblProteinID = None
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
                        uniprotSet.add(
                            UniProtRow(symbol, symbolSynonyms, entrezID, ensemblID, uniprotID, ensemblProteinID))
                    elif len(symbols) == 1 and len(entrezIDs) <= 1:
                        symbol = symbols[0]
                        symbolSynonyms = symbolSynonymsDict[symbol]
                        entrezID = entrezIDs[0] if entrezIDs else None
                        uniprotSet.add(
                            UniProtRow(symbol, symbolSynonyms, entrezID, None, uniprotID, ensemblProteinID))
                    elif len(symbols) == 1 and len(ensemblIDs) <= 1:
                        symbol = symbols[0]
                        symbolSynonyms = symbolSynonymsDict[symbol]
                        ensemblID = ensemblIDs[0] if ensemblIDs else None
                        uniprotSet.add(
                            UniProtRow(symbol, symbolSynonyms, None, ensemblID, uniprotID, ensemblProteinID))
                    elif len(symbols) > 1:
                        for symbol in symbols:
                            symbolSynonyms = symbolSynonymsDict[symbol]
                            uniprotSet.add(UniProtRow(symbol, symbolSynonyms, None, None, uniprotID, ensemblProteinID))
                    symbols = []
                    symbolSynonymsDict = {}
                    entrezIDs = []
                    ensemblIDs = []
                elif valueType == "UniProtKB-ID" and ensemblProteinID is not None:
                    uniprotSet.add(UniProtRow(None, [], None, None, uniprotID, ensemblProteinID))
                elif valueType == "STRING":
                    ensemblProteinID = value.split(".")[1]
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
