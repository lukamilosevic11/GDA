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

from GDA_backend.Classes.attributes import EntrezID, UniprotID, EnsemblID, DOID, DiseaseName, Xrefs
from GDA_backend.Classes.search_engine_client import SearchEngineClient
from GDA_backend.Common.constants import COLLECTION_NAME_DOID, DISEASE_NAME_DOID_JSONL_PATH
from GDA_backend.Common.init import Source, Xref, XREFS_SOURCE, json, Progress, SpinnerColumn, TimeElapsedColumn, \
    TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn
from GDA_backend.Common.util import PreprocessingDiseaseName


class AnnotationContext:
    def __init__(self, dbContext, createCollection, totalProgress):
        self.__dbContext = dbContext
        self.__searchEngineClient = SearchEngineClient()
        self.__sources = Source.GetAllSources()
        self.totalProgress = totalProgress

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
        self.__omimToDOID = {}
        self.__umlsToDOID = {}
        self.__meshToDOID = {}
        self.__gardToDOID = {}
        self.__medDraToDOID = {}
        self.__icd10ToDOID = {}

        # DiseaseName
        self.__doidToDiseaseName = {}
        self.__doidToParentDoidAndDiseaseName = {}  # Doid -> list((Doid, DiseaseName))
        self.__orphaToDiseaseName = {}
        self.__omimToDiseaseName = {}  # Omim -> list(DiseaseName)
        self.__omimToDoidAndDiseaseName = {}  # Omim -> list((Doid, DiseaseName))

        # Xrefs
        self.__orphaToExactXrefs = {}  # Orpha -> dict(xrefs)
        self.__orphaToBtntXrefs = {}  # Orpha -> dict(xrefs)
        self.__orphaToNtbtXrefs = {}  # Orpha -> dict(xrefs)
        self.__orphaToOtherXrefs = {}  # Orpha -> dict(xrefs)

        # Search Engine set{(diseaseName, definition, DOID)}
        self.__searchEngineSet = set()

        self.__InitializeDictionaries()
        self.__InitializeSearchEngineClient(createCollection)
        self.__InitializeAttributes()

    def __InitializeOrphanetXrefDictionaries(self, progress, progressTask):
        sourceSet = self.__dbContext.GetDatabaseBySource(Source.ORPHANET_XREF)
        for term in sourceSet:
            progress.update(progressTask, advance=1)
            if self.totalProgress is not None:
                self.totalProgress.increase_step()

            if term.orpha is not None:
                # Orpha -> Xrefs
                exactXrefs = term.GetExactXrefs()
                btntXrefs = term.GetBtntXrefs()
                ntbtXrefs = term.GetNtbtXrefs()
                otherXrefs = term.GetOtherXrefs()
                if exactXrefs and term.orpha not in self.__orphaToExactXrefs:
                    self.__orphaToExactXrefs[term.orpha] = exactXrefs

                if btntXrefs and term.orpha not in self.__orphaToBtntXrefs:
                    self.__orphaToBtntXrefs[term.orpha] = btntXrefs

                if ntbtXrefs and term.orpha not in self.__orphaToNtbtXrefs:
                    self.__orphaToNtbtXrefs[term.orpha] = ntbtXrefs

                if otherXrefs and term.orpha not in self.__orphaToOtherXrefs:
                    self.__orphaToOtherXrefs[term.orpha] = otherXrefs

                # Orpha -> Disease Name
                if term.orpha not in self.__orphaToDiseaseName and term.diseaseName is not None:
                    self.__orphaToDiseaseName[term.orpha] = term.diseaseName

    def __InitializeDictionaries(self):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(),
                      TaskProgressColumn(), MofNCompleteColumn(),
                      TimeElapsedColumn(), TimeRemainingColumn()) as progress:
            progressTask = progress.add_task("Preparing for parsing", total=self.__dbContext.GetAllSourcesLength())
            self.__InitializeOrphanetXrefDictionaries(progress, progressTask)
            for source in self.__sources:
                if source is Source.ORPHANET_XREF:
                    continue

                sourceSet = self.__dbContext.GetDatabaseBySource(source)
                for term in sourceSet:
                    progress.update(progressTask, advance=1)
                    if self.totalProgress is not None:
                        self.totalProgress.increase_step()

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

                    # Symbol (for additional Uniprot and HUGO symbol synonyms)
                    if source is Source.UNIPROT or source is Source.HUGO:
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

                                # Search Engine Set
                                preprocessedDiseaseName = ' '.join(preprocessedDiseaseName)
                                definition = (PreprocessingDiseaseName(term.definition, True)
                                              if term.definition is not None else "") if source is Source.OBO else ""
                                self.__searchEngineSet.add((preprocessedDiseaseName, definition, term.doid))

                    # DiseaseName -> DOID (OBO synonyms) and xrefs -> DOID and DOID -> ParentDoidAndDiseaseName
                    if source is Source.OBO:
                        # DOID -> ParentDoidAndDiseaseName
                        parentDoidAndDiseaseNames = term.GetParentDiseaseNameAndDoids()
                        if parentDoidAndDiseaseNames and term.doid is not None:
                            self.__doidToParentDoidAndDiseaseName[term.doid] = parentDoidAndDiseaseNames

                        # DiseaseName -> DOID (OBO synonyms)
                        diseaseNameSynonyms = term.GetSynonyms()
                        if diseaseNameSynonyms and term.doid is not None:
                            for diseaseNameSynonym in diseaseNameSynonyms:
                                preprocessedDiseaseNameSynonym = PreprocessingDiseaseName(diseaseNameSynonym)
                                preprocessedDiseaseNameSynonymFrozenSet = \
                                    frozenset(preprocessedDiseaseNameSynonym)
                                if preprocessedDiseaseNameSynonymFrozenSet not in self.__diseaseNameFrozenSetToDOID:
                                    self.__diseaseNameFrozenSetToDOID[preprocessedDiseaseNameSynonymFrozenSet] = \
                                        term.doid

                                # Search Engine Set
                                preprocessedDiseaseNameSynonym = ' '.join(preprocessedDiseaseNameSynonym)
                                definition = PreprocessingDiseaseName(term.definition, True) \
                                    if term.definition is not None else ""
                                self.__searchEngineSet.add((preprocessedDiseaseNameSynonym, definition, term.doid))

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

                diseaseNamePreprocessed = set(PreprocessingDiseaseName(diseaseName))
                # Omim -> Disease Name
                if diseaseName is not None:
                    if value not in self.__omimToDiseaseName:
                        self.__omimToDiseaseName[value] = [diseaseName]
                    elif diseaseName not in self.__omimToDiseaseName[value]:
                        omimDiseaseNames = list(map(lambda x: set(PreprocessingDiseaseName(x)),
                                                    self.__omimToDiseaseName[value]))
                        if diseaseNamePreprocessed not in omimDiseaseNames:
                            self.__omimToDiseaseName[value].append(diseaseName)

                # Omim -> Doid and Disease Name
                if diseaseName is not None and doid is not None:
                    if value not in self.__omimToDoidAndDiseaseName:
                        self.__omimToDoidAndDiseaseName[value] = [(doid, diseaseName)]
                    elif (doid, diseaseName) not in self.__omimToDoidAndDiseaseName[value]:
                        omimDoidAndDiseaseNames = \
                            list(map(lambda x: (x[0], set(PreprocessingDiseaseName(x[1]))),
                                     self.__omimToDoidAndDiseaseName[value]))
                        if (doid, diseaseNamePreprocessed) not in omimDoidAndDiseaseNames:
                            self.__omimToDoidAndDiseaseName[value].append((doid, diseaseName))
                            self.__omimToDoidAndDiseaseName[value].sort(key=lambda x: x[0])

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
        self.diseaseName = DiseaseName(self.__doidToDiseaseName, self.__orphaToDiseaseName, self.__omimToDiseaseName,
                                       self.__omimToDoidAndDiseaseName, self.__doidToParentDoidAndDiseaseName)
        self.xrefs = Xrefs(self.__orphaToExactXrefs, self.__orphaToBtntXrefs, self.__orphaToNtbtXrefs,
                           self.__orphaToOtherXrefs)

    def __InitializeSearchEngineClient(self, createCollection):
        try:
            collections = self.__searchEngineClient.GetAllCollections()
            collectionExist = False
            for collection in collections:
                if collection["name"] == COLLECTION_NAME_DOID:
                    collectionExist = True

            if collectionExist and createCollection:
                self.__searchEngineClient.DeleteCollection(COLLECTION_NAME_DOID)

            if createCollection or not collectionExist:
                self.__searchEngineClient.CreateCollection(COLLECTION_NAME_DOID,
                                                           [
                                                               {'name': 'diseaseName', 'type': 'string'},
                                                               {'name': 'definition', 'type': 'string'},
                                                               {'name': 'doid', 'type': 'string'}
                                                           ])
                with open(DISEASE_NAME_DOID_JSONL_PATH, 'w') as jsonlFile:
                    for diseaseName, definition, doid in self.__searchEngineSet:
                        jsonRow = {
                            "diseaseName": diseaseName,
                            "definition": definition,
                            "doid": doid
                        }
                        json.dump(jsonRow, jsonlFile)
                        jsonlFile.write('\n')

                self.__searchEngineClient.ImportDataFromFile(COLLECTION_NAME_DOID, DISEASE_NAME_DOID_JSONL_PATH)
        except Exception as e:
            print(e)
