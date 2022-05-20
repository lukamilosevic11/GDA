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

from Classes.search_engine_client import SearchEngineClient
from Common.constants import COLLECTION_NAME_DOID, QUERY_BY_DOID, DISEASE_NAME_DOID_JSONL_PATH
from Common.init import Source
from Common.util import PreprocessingDiseaseName, WriteDictToJsonlFile, JaccardSimilarity


class AnnotationContext:
    def __init__(self, dbContext, dropCollection):
        self.__dbContext = dbContext
        self.__searchEngineClient = SearchEngineClient()
        self.__sources = Source.GetAllSources()

        # Attributes
        self.entrezID = None
        self.uniprotID = None
        self.ensemblID = None
        self.doid = None
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

        # DOID
        self.__diseaseNameFrozenSetToDOID = {}
        self.__diseaseNameToDOID = {}

        # DiseaseName
        self.__symbolToDiseaseName = {}
        self.__entrezIDToDiseaseName = {}
        self.__ensemblIDToDiseaseName = {}
        self.__doidToDiseaseName = {}

        self.__InitializeDictionaries()
        self.__InitializeSearchEngineClient(dropCollection)
        self.__InitializeAttributes()

    def __InitializeDictionaries(self):
        for source in self.__sources:
            sourceSet = self.__dbContext.GetDatabaseBySource(source)
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

                # DiseaseName
                if term.diseaseName is not None:
                    # DiseaseName -> DOID
                    if source is Source.DISEASES or source is Source.OBO:
                        if term.doid is not None:
                            preprocessedDiseaseName = PreprocessingDiseaseName(term.diseaseName)
                            preprocessedDiseaseNameFrozenSet = frozenset(preprocessedDiseaseName)
                            if preprocessedDiseaseNameFrozenSet not in self.__diseaseNameFrozenSetToDOID:
                                self.__diseaseNameFrozenSetToDOID[preprocessedDiseaseNameFrozenSet] = term.doid

                            preprocessedDiseaseName = ' '.join(preprocessedDiseaseName)
                            if preprocessedDiseaseName not in self.__diseaseNameToDOID:
                                self.__diseaseNameToDOID[preprocessedDiseaseName] = term.doid

                    # DiseaseName -> DOID (OBO synonyms)
                    if source is Source.OBO:
                        diseaseNameSynonyms = term.getSynonyms()
                        if diseaseNameSynonyms:
                            for diseaseNameSynonym in diseaseNameSynonyms:
                                if term.doid is not None:
                                    preprocessedDiseaseNameSynonym = PreprocessingDiseaseName(diseaseNameSynonym)
                                    preprocessedDiseaseNameSynonymFrozenSet = \
                                        frozenset(preprocessedDiseaseNameSynonym)
                                    if preprocessedDiseaseNameSynonymFrozenSet not in self.__diseaseNameFrozenSetToDOID:
                                        self.__diseaseNameFrozenSetToDOID[preprocessedDiseaseNameSynonymFrozenSet] = \
                                            term.doid

                                    preprocessedDiseaseNameSynonym = ' '.join(preprocessedDiseaseNameSynonym)
                                    if preprocessedDiseaseNameSynonym not in self.__diseaseNameToDOID:
                                        self.__diseaseNameToDOID[preprocessedDiseaseNameSynonym] = term.doid

    def __InitializeAttributes(self):
        self.entrezID = EntrezID(self.__symbolToEntrezID, self.__ensemblIDToEntrezID, self.__uniprotIDToEntrezID)
        self.uniprotID = UniprotID(self.__symbolToUniprotID, self.__entrezIDToUniprotID, self.__ensemblIDToUniprotID)
        self.ensemblID = EnsemblID(self.__symbolToEnsemblID, self.__entrezIDToEnsemblID, self.__uniprotIDToEnsemblID)
        self.doid = DOID(self.__diseaseNameFrozenSetToDOID, self.__searchEngineClient)
        self.diseaseName = DiseaseName(self.__symbolToDiseaseName, self.__entrezIDToDiseaseName,
                                       self.__ensemblIDToDiseaseName, self.__doidToDiseaseName)

    def __InitializeSearchEngineClient(self, dropCollection):
        try:
            if dropCollection:
                self.__searchEngineClient.DeleteCollection(COLLECTION_NAME_DOID)

            collections = self.__searchEngineClient.GetAllCollections()
            createCollection = True
            insertDocuments = True
            for collection in collections:
                if collection["name"] == COLLECTION_NAME_DOID:
                    createCollection = False
                    insertDocuments = True if collection["num_documents"] < len(self.__diseaseNameToDOID) else False

            if createCollection:
                self.__searchEngineClient.CreateCollection(COLLECTION_NAME_DOID,
                                                           [
                                                               {'name': 'diseaseName', 'type': 'string'},
                                                               {'name': 'doid', 'type': 'string'}
                                                           ])
            if insertDocuments:
                WriteDictToJsonlFile(DISEASE_NAME_DOID_JSONL_PATH, self.__diseaseNameToDOID, "diseaseName", "doid")
                self.__searchEngineClient.ImportDataFromFile(COLLECTION_NAME_DOID, DISEASE_NAME_DOID_JSONL_PATH)
        except:
            print("Collection already exist")


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


# DOID is part of: Diseases, OBO
# DOID can be found using diseaseName
class DOID:
    def __init__(self, diseaseNameFrozenSetDict, searchEngineClient):
        self.__searchEngineClient = searchEngineClient
        self.__diseaseNameFrozenSetDict = diseaseNameFrozenSetDict

    def GetByDiseaseName(self, diseaseName):
        if diseaseName is None:
            return None

        preprocessedDiseaseName = PreprocessingDiseaseName(diseaseName)
        preprocessedDiseaseNameFrozenSet = frozenset(preprocessedDiseaseName)
        if preprocessedDiseaseNameFrozenSet in self.__diseaseNameFrozenSetDict:
            return self.__diseaseNameFrozenSetDict[preprocessedDiseaseNameFrozenSet]
        else:
            return self.__SearchWithSearchEngine(' '.join(preprocessedDiseaseName))

    # TODO: add check if we have more than one hit then we can compare results with Jaccard index or some other measure
    def __SearchWithSearchEngine(self, preprocessedDiseaseName):
        searchResult = self.__searchEngineClient. \
            SearchByQuery(COLLECTION_NAME_DOID, preprocessedDiseaseName, QUERY_BY_DOID)
        if len(searchResult["hits"]) > 0:
            # foundDiseaseName = searchResult["hits"][0]["document"]["diseaseName"]
            # jaccSimiliarity = jaccardSimilarity(foundDiseaseName, preprocessedDiseaseName)
            return searchResult["hits"][0]["document"]["doid"]
        elif " due " in preprocessedDiseaseName:
            return self.__SearchWithSearchEngine(preprocessedDiseaseName.split(" due ")[0])
        elif " with without " in preprocessedDiseaseName:
            return self.__SearchWithSearchEngine(preprocessedDiseaseName.split(" with without ")[0])
        elif " with " in preprocessedDiseaseName:
            return self.__SearchWithSearchEngine(preprocessedDiseaseName.split(" with ")[0])
        elif " without " in preprocessedDiseaseName:
            return self.__SearchWithSearchEngine(preprocessedDiseaseName.split(" without ")[0])

        return None


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
