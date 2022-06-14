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

from Classes.attributes import EntrezID, UniprotID, EnsemblID, DOID, DiseaseName, Xrefs
from Classes.search_engine_client import SearchEngineClient
from Common.constants import COLLECTION_NAME_DOID, DISEASE_NAME_DOID_JSONL_PATH
from Common.init import Source, Xref, XREFS_SOURCE
from Common.util import PreprocessingDiseaseName, WriteDictToJsonlFile, PreprocessingDiseaseNameLight


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
        self.xrefs = None

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
        self.__omimToDOID = {}
        self.__umlsToDOID = {}
        self.__meshToDOID = {}
        self.__gardToDOID = {}
        self.__medDraToDOID = {}
        self.__icd10ToDOID = {}

        # DiseaseName
        self.__doidToDiseaseName = {}
        self.__orphaToDiseaseName = {}
        self.__omimToDiseaseName = {}  # Omim -> list(DiseaseName)

        # Xrefs
        self.__orphaToExactXrefs = {}  # Orpha -> dict(xrefs)
        self.__orphaToNotExactXrefs = {}  # Orpha -> dict(xrefs)
        self.__orphaToXrefs = {}  # Orpha -> dict(xrefs)

        self.__InitializeDictionaries()
        self.__InitializeSearchEngineClient(dropCollection)
        self.__InitializeAttributes()

    def __InitializeOrphanetXrefDictionaries(self):
        sourceSet = self.__dbContext.GetDatabaseBySource(Source.ORPHANET_XREF)
        for term in sourceSet:
            # Orpha
            if term.orpha is not None:
                # Orpha -> Xrefs
                if term.orpha not in self.__orphaToExactXrefs:
                    exactXrefs = term.GetExactXrefs()
                    notExactXrefs = term.GetNotExactXrefs()
                    xrefs = term.GetXrefs()
                    if exactXrefs:
                        self.__orphaToExactXrefs[term.orpha] = exactXrefs

                    if notExactXrefs:
                        self.__orphaToNotExactXrefs[term.orpha] = notExactXrefs

                    if xrefs:
                        self.__orphaToXrefs[term.orpha] = xrefs

                # Orpha -> Disease Name
                if term.orpha not in self.__orphaToDiseaseName and term.diseaseName is not None:
                    self.__orphaToDiseaseName[term.orpha] = term.diseaseName

    def __InitializeDictionaries(self):
        self.__InitializeOrphanetXrefDictionaries()
        for source in self.__sources:
            if source is Source.ORPHANET_XREF:
                continue

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

                # DOID
                if term.doid is not None:
                    # DOID -> DiseaseName
                    if term.doid not in self.__doidToDiseaseName and term.diseaseName is not None:
                        self.__doidToDiseaseName[term.doid] = term.diseaseName

                    # DOID -> Synonym(additional disease name synonyms from OBO)
                    if source is Source.OBO and term.doid not in self.__doidToDiseaseName:
                        diseaseNameSynonyms = term.GetSynonyms()
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

                # DiseaseName -> DOID (OBO synonyms) and xrefs -> DOID
                if source is Source.OBO:
                    diseaseNameSynonyms = term.GetSynonyms()
                    if diseaseNameSynonyms and term.doid is not None:
                        for diseaseNameSynonym in diseaseNameSynonyms:
                            preprocessedDiseaseNameSynonym = PreprocessingDiseaseName(diseaseNameSynonym)
                            preprocessedDiseaseNameSynonymFrozenSet = \
                                frozenset(preprocessedDiseaseNameSynonym)
                            if preprocessedDiseaseNameSynonymFrozenSet not in self.__diseaseNameFrozenSetToDOID:
                                self.__diseaseNameFrozenSetToDOID[preprocessedDiseaseNameSynonymFrozenSet] = \
                                    term.doid

                            preprocessedDiseaseNameSynonym = ' '.join(preprocessedDiseaseNameSynonym)
                            if preprocessedDiseaseNameSynonym not in self.__diseaseNameToDOID:
                                self.__diseaseNameToDOID[preprocessedDiseaseNameSynonym] = term.doid

                    # xrefs -> DOID
                    xrefs = term.GetXrefs()
                    for xref in xrefs:
                        xrefSplitted = xref.id.split(':')
                        if len(xrefSplitted) != 2:
                            continue

                        xref = xrefSplitted[0].strip()
                        value = xrefSplitted[1].strip()
                        self.__AddXrefValue(xref, value, term.doid, term.diseaseName)

                    alternateIds = term.GetAlternateIds()
                    for alternateId in alternateIds:
                        alternateIdSplitted = alternateId.split(':')
                        if len(alternateIdSplitted) != 2:
                            continue

                        xref = alternateIdSplitted[0].strip()
                        value = alternateIdSplitted[1].strip()
                        self.__AddXrefValue(xref, value, term.doid, term.diseaseName)

    def __AddXrefValue(self, xref, value, doid, diseaseName):
        if xref in XREFS_SOURCE:
            xrefSource = XREFS_SOURCE[xref]
            if xrefSource == Xref.OMIM:
                # Omim -> DOID
                if doid is not None and value not in self.__omimToDOID:
                    self.__omimToDOID[value] = doid

                # Omim -> Disease Name
                if diseaseName is not None:
                    if value not in self.__omimToDiseaseName:
                        self.__omimToDiseaseName[value] = [diseaseName]
                    elif diseaseName not in self.__omimToDiseaseName[value]:
                        omimDiseaseNames = list(map(PreprocessingDiseaseNameLight, self.__omimToDiseaseName[value]))
                        diseaseNamePreprocessed = PreprocessingDiseaseNameLight(diseaseName)
                        if diseaseNamePreprocessed not in omimDiseaseNames:
                            self.__omimToDiseaseName[value].append(diseaseName)

            elif xrefSource == Xref.UMLS and value not in self.__umlsToDOID and doid is not None:
                self.__umlsToDOID[value] = doid
            elif xrefSource == Xref.MeSH and value not in self.__meshToDOID and doid is not None:
                self.__meshToDOID[value] = doid
            elif xrefSource == Xref.GARD and value not in self.__gardToDOID and doid is not None:
                self.__gardToDOID[value] = doid
            elif xrefSource == Xref.MedDRA and value not in self.__medDraToDOID and doid is not None:
                self.__medDraToDOID[value] = doid
            elif xrefSource == Xref.ICD10 and value not in self.__icd10ToDOID and doid is not None:
                self.__icd10ToDOID[value] = doid

    def __InitializeAttributes(self):
        self.entrezID = EntrezID(self.__symbolToEntrezID, self.__ensemblIDToEntrezID, self.__uniprotIDToEntrezID)
        self.uniprotID = UniprotID(self.__symbolToUniprotID, self.__entrezIDToUniprotID, self.__ensemblIDToUniprotID)
        self.ensemblID = EnsemblID(self.__symbolToEnsemblID, self.__entrezIDToEnsemblID, self.__uniprotIDToEnsemblID)
        self.doid = DOID(self.__searchEngineClient, self.__diseaseNameFrozenSetToDOID, self.__omimToDOID,
                         self.__umlsToDOID, self.__meshToDOID, self.__gardToDOID, self.__medDraToDOID,
                         self.__icd10ToDOID)
        self.diseaseName = DiseaseName(self.__doidToDiseaseName, self.__orphaToDiseaseName, self.__omimToDiseaseName)
        self.xrefs = Xrefs(self.__orphaToExactXrefs, self.__orphaToNotExactXrefs, self.__orphaToXrefs)

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
