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
from Common.init import Source


class AnnotationContext:
    def __init__(self, dbContext):
        self.dbContext = dbContext
        self.sources = Source.GetAllSources()

        # Fields
        self.entrezID = None
        self.uniprotID = None
        self.ensemblID = None
        self.diseaseName = None

        # Dictionaries
        # EntrezID
        self.__symbolToEntrezID = {}
        self.__ensemblIDToEntrezID = {}
        self.__uniprotIDToEntrezID = {}

        # UniprotID
        self.__symbolToUniprotID = {}
        self.__entrezIDToUniprotID = {}
        self.__ensemblIDToUniprotID = {}

        # EnsemblID
        self.__symbolToEnsemblID = {}
        self.__entrezIDToEnsemblID = {}
        self.__uniprotIDToEnsemblID = {}

        # DiseaseName
        self.__symbolToDiseaseName = {}
        self.__entrezIDToDiseaseName = {}
        self.__ensemblIDToDiseaseName = {}
        self.__doidToDiseaseName = {}

        self.InitializeDictionaries()
        self.InitializeFields()

    def InitializeDictionaries(self):
        for source in self.sources:
            sourceSet = self.dbContext.GetDatabaseBySource(source)
            for term in sourceSet:
                # Symbol
                if term.symbol is not None:
                    # Symbol -> EntrezID
                    if term.symbol not in self.__symbolToEntrezID and term.entrezID is not None:
                        self.__symbolToEntrezID[term.symbol] = term.entrezID
                    # Symbol -> UniprotID
                    if term.symbol not in self.__symbolToUniprotID and term.uniprotID is not None:
                        self.__symbolToUniprotID[term.symbol] = term.uniprotID
                    # Symbol -> EnsemblID
                    if term.symbol not in self.__symbolToEnsemblID and term.ensemblID is not None:
                        self.__symbolToEnsemblID[term.symbol] = term.ensemblID
                    # Symbol -> DiseaseName
                    if term.symbol not in self.__symbolToDiseaseName and term.diseaseName is not None:
                        self.__symbolToDiseaseName[term.symbol] = term.diseaseName

                # Symbol (for additional Uniprot symbol synonyms)
                if source is Source.UNIPROT:
                    symbolSynonyms = term.getSymbolSynonyms()
                    if symbolSynonyms:
                        for symbol in symbolSynonyms:
                            # Symbol -> EntrezID
                            if symbol not in self.__symbolToEntrezID and term.entrezID is not None:
                                self.__symbolToEntrezID[symbol] = term.entrezID
                            # Symbol -> UniprotID
                            if symbol not in self.__symbolToUniprotID and term.uniprotID is not None:
                                self.__symbolToUniprotID[symbol] = term.uniprotID
                            # Symbol -> EnsemblID
                            if symbol not in self.__symbolToEnsemblID and term.ensemblID is not None:
                                self.__symbolToEnsemblID[symbol] = term.ensemblID

                # EntrezID
                if term.entrezID is not None:
                    # EntrezID -> UniprotID
                    if term.entrezID not in self.__entrezIDToUniprotID and term.uniprotID is not None:
                        self.__entrezIDToUniprotID[term.entrezID] = term.uniprotID
                    # EntrezID -> EnsemblID
                    if term.entrezID not in self.__entrezIDToEnsemblID and term.ensemblID is not None:
                        self.__entrezIDToEnsemblID[term.entrezID] = term.ensemblID
                    # EntrezID -> DiseaseName
                    if term.entrezID not in self.__entrezIDToDiseaseName and term.diseaseName is not None:
                        self.__entrezIDToDiseaseName[term.entrezID] = term.diseaseName

                # UniprotID
                if term.uniprotID is not None:
                    # UniprotID -> EntrezID
                    if term.uniprotID not in self.__uniprotIDToEntrezID and term.entrezID is not None:
                        self.__uniprotIDToEntrezID[term.uniprotID] = term.entrezID
                    # UniprotID -> EnsemblID
                    if term.uniprotID not in self.__uniprotIDToEnsemblID and term.ensemblID is not None:
                        self.__uniprotIDToEnsemblID[term.uniprotID] = term.ensemblID

                # TODO: implement early out of the loop using break if we have
                # TODO: term.symbol in self.__symbolToUniprotID and term.entrezID in self.__entrezIDToUniprotID and ...
                # UniprotID (additional UniprotIDs from Hugo)
                if source is Source.HUGO:
                    uniprotIDs = term.getUniprotIDs()
                    for uniprotID in uniprotIDs:
                        # Symbol -> UniprotID
                        if term.symbol not in self.__symbolToUniprotID and term.symbol is not None:
                            self.__symbolToUniprotID[term.symbol] = uniprotID

                        # EntrezID -> UniprotID
                        if term.entrezID not in self.__entrezIDToUniprotID and term.entrezID is not None:
                            self.__entrezIDToUniprotID[term.entrezID] = uniprotID

                        # EnsemblID -> UniprotID
                        if term.ensemblID not in self.__ensemblIDToUniprotID and term.ensemblID is not None:
                            self.__ensemblIDToUniprotID[term.ensemblID] = uniprotID

                        # UniprotID -> EntrezID
                        if uniprotID not in self.__uniprotIDToEntrezID and term.entrezID is not None:
                            self.__uniprotIDToEntrezID[uniprotID] = term.entrezID

                        # UniprotID -> EnsemblID
                        if uniprotID not in self.__uniprotIDToEnsemblID and term.ensemblID is not None:
                            self.__uniprotIDToEnsemblID[uniprotID] = term.ensemblID

                # EnsemblID
                if term.ensemblID is not None:
                    # EnsemblID -> EntrezID
                    if term.ensemblID not in self.__ensemblIDToEntrezID and term.entrezID is not None:
                        self.__ensemblIDToEntrezID[term.ensemblID] = term.entrezID
                    # EnsemblID -> UniprotID
                    if term.ensemblID not in self.__ensemblIDToUniprotID and term.uniprotID is not None:
                        self.__ensemblIDToUniprotID[term.ensemblID] = term.uniprotID
                    # EnsemblID -> DiseaseName
                    if term.ensemblID not in self.__ensemblIDToDiseaseName and term.diseaseName is not None:
                        self.__ensemblIDToDiseaseName[term.ensemblID] = term.diseaseName

                # DOID
                if term.doid is not None:
                    # DOID -> DiseaseName
                    if term.doid not in self.__doidToDiseaseName and term.diseaseName is not None:
                        self.__doidToDiseaseName[term.doid] = term.diseaseName

                    # DOID -> Synonym(additional disease name synonyms from OBO)
                    if source is Source.OBO and term.doid not in self.__doidToDiseaseName:
                        diseaseNameSynonyms = term.getSynonyms()
                        if diseaseNameSynonyms:
                            self.__doidToDiseaseName[term.doid] = diseaseNameSynonyms[0]

    def InitializeFields(self):
        self.entrezID = EntrezID(self.__symbolToEntrezID, self.__ensemblIDToEntrezID, self.__uniprotIDToEntrezID)
        self.uniprotID = UniprotID(self.__symbolToUniprotID, self.__entrezIDToUniprotID, self.__ensemblIDToUniprotID)
        self.ensemblID = EnsemblID(self.__symbolToEnsemblID, self.__entrezIDToEnsemblID, self.__uniprotIDToEnsemblID)
        self.diseaseName = DiseaseName(self.__symbolToDiseaseName, self.__entrezIDToDiseaseName,
                                       self.__ensemblIDToDiseaseName, self.__doidToDiseaseName)


# EntrezID is part of: DisGeNet, Cosmic, ClinVar, HPO, Uniprot, Hugo
# EntrezID can be found using symbol, ensemblID and uniprotID
class EntrezID:
    def __init__(self, symbolDict, ensemblIDDict, uniprotIDDict):
        self.__symbolDict = symbolDict
        self.__ensemblIDDict = ensemblIDDict
        self.__uniprotIDDict = uniprotIDDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEnsemblID(self, ensemblID):
        return self.__ensemblIDDict[ensemblID] if ensemblID in self.__ensemblIDDict else None

    def GetByUniprotID(self, uniprotID):
        return self.__uniprotIDDict[uniprotID] if uniprotID in self.__uniprotIDDict else None


# UniprotID is part of: Uniprot, Hugo
# UniprotID can be found using symbol, entrezID and ensemblID
class UniprotID:
    def __init__(self, symbolDict, entrezIDDict, ensemblIDDict):
        self.__symbolDict = symbolDict
        self.__entrezIDDict = entrezIDDict
        self.__ensemblIDDict = ensemblIDDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEntrezID(self, entrezID):
        return self.__entrezIDDict[entrezID] if entrezID in self.__entrezIDDict else None

    def GetByEnsemblID(self, ensemblID):
        return self.__ensemblIDDict[ensemblID] if ensemblID in self.__ensemblIDDict else None


# EnsemblID is part of: Orphanet ,Uniprot, Hugo
# EnsemblID can be found using symbol, entrezID and uniprotID
class EnsemblID:
    def __init__(self, symbolDict, entrezIDDict, uniprotIDDict):
        self.__symbolDict = symbolDict
        self.__entrezIDDict = entrezIDDict
        self.__uniprotIDDict = uniprotIDDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEntrezID(self, entrezID):
        return self.__entrezIDDict[entrezID] if entrezID in self.__entrezIDDict else None

    def GetByUniprotID(self, uniprotID):
        return self.__uniprotIDDict[uniprotID] if uniprotID in self.__uniprotIDDict else None


# DiseaseName is part of: DisGeNet, Cosmic, HumsaVar, Orphanet, ClinVar, Diseases, OBO
# DiseaseName can be found using symbol, entrezID, ensemblID and DOID
class DiseaseName:
    def __init__(self, symbolDict, entrezIDDict, ensemblIDDict, doidDict):
        self.__symbolDict = symbolDict
        self.__entrezIDDict = entrezIDDict
        self.__ensemblIDDict = ensemblIDDict
        self.__doidDict = doidDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEntrezID(self, entrezID):
        return self.__entrezIDDict[entrezID] if entrezID in self.__entrezIDDict else None

    def GetByEnsemblID(self, ensemblID):
        return self.__ensemblIDDict[ensemblID] if ensemblID in self.__ensemblIDDict else None

    def GetByDoid(self, doid):
        return self.__doidDict[doid] if doid in self.__doidDict else None
