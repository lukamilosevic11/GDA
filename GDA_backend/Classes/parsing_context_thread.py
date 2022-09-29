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

from GDA_backend.Classes.annotation_context import AnnotationContext
from GDA_backend.Classes.annotation_models import AnnotationRowOutput
from GDA_backend.Classes.db_context import DBContext
from GDA_backend.Common.constants import DOID_SOURCE_DATABASE, ANNOTATION_FILE_HEADER, DOID_SOURCE_XREF_OMIM
from GDA_backend.Common.init import Source, partial, Attribute, permutations, time, ThreadPoolExecutor, Progress, \
    SpinnerColumn, \
    TimeElapsedColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn
from GDA_backend.Common.util import GetAttribute, WriteStructureToFile, JaccardSimilarity, PreprocessingDiseaseName, \
    PrintElapsedTime, PreprocessAttribute


class ParsingContextThread:
    def __init__(self, progress, createCollection, searchEngineHostName="localhost"):
        dbContextStartTime = time.time()
        self.dbContext = DBContext()
        PrintElapsedTime(dbContextStartTime, time.time(), "Reading sources elapsed time")
        annotationContextStartTime = time.time()
        if progress is not None:
            progress.set_total(self.dbContext.GetTotalParsingLength() + self.dbContext.GetAllSourcesLength())

        self.annotationContext = AnnotationContext(self.dbContext, createCollection, progress, searchEngineHostName)
        PrintElapsedTime(annotationContextStartTime, time.time(), "Preparing parsing elapsed time")
        self.__sources = Source.GetSourcesForParsing()
        self.__sourcesAnnotationSetDict = {}
        self.__annotationSet = set()
        parsingSourcesStartTime = time.time()
        self.__ParseSources(progress)
        PrintElapsedTime(parsingSourcesStartTime, time.time(), "Parsing sources elapsed time")
        self.__CreateFullAnnotationSet()

    def __ParseSource(self, source, progress, progressBar, parsingTask):
        sourceSet = set()
        sourceName = Source.GetSourceName(source)
        sourceDB = self.dbContext.GetDatabaseBySource(source)
        sourceTask = progressBar.add_task(sourceName, total=len(sourceDB))
        for term in sourceDB:
            # Phase I
            progressBar.update(parsingTask, advance=1)
            progressBar.update(sourceTask, advance=1)
            symbol = term.symbol
            entrezID = term.entrezID
            uniprotID = term.uniprotID
            ensemblID = term.ensemblID
            doid = term.doid
            diseaseName = term.diseaseName
            doidSource = DOID_SOURCE_DATABASE if source is Source.DISEASES and doid is not None else None
            doidAndDiseaseNames = []

            # Part of Phase II moved here because of initialization of foundAttributes and noneAttributes
            # Only for Diseases to find EntrezID, UniprotID and EnsemblID by EnsemblProteinID
            if source is Source.DISEASES and term.ensemblProteinID is not None:
                if term.entrezID is None:
                    entrezID = self.annotationContext.entrezID.GetByEnsemblProteinID(
                        PreprocessAttribute(term.ensemblProteinID))

                if term.uniprotID is None:
                    uniprotID = self.annotationContext.uniprotID.GetByEnsemblProteinID(
                        PreprocessAttribute(term.ensemblProteinID))

                if term.ensemblID is None:
                    ensemblID = self.annotationContext.ensemblID.GetByEnsemblProteinID(
                        PreprocessAttribute(term.ensemblProteinID))

            noneAttributes = []
            if symbol is None:
                noneAttributes.append(Attribute.SYMBOL)
            if entrezID is None:
                noneAttributes.append(Attribute.ENTREZ_ID)
            if uniprotID is None:
                noneAttributes.append(Attribute.UNIPROT_ID)
            if ensemblID is None:
                noneAttributes.append(Attribute.ENSEMBL_ID)

            def partialGetMethodsSymbol(entrezIDP, uniprotIDP, ensemblIDP):
                partialMethods = []
                if entrezIDP is not None:
                    partialMethods.append(partial(self.annotationContext.symbol.GetByEntrezID, entrezIDP))

                if uniprotIDP is not None:
                    partialMethods.append(partial(self.annotationContext.symbol.GetByUniProtID, uniprotIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(self.annotationContext.symbol.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsEntrezID(symbolP, uniprotIDP, ensemblIDP):
                partialMethods = []
                if symbolP is not None:
                    partialMethods.append(partial(self.annotationContext.entrezID.GetBySymbol, symbolP))

                if uniprotIDP is not None:
                    partialMethods.append(partial(self.annotationContext.entrezID.GetByUniProtID, uniprotIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(self.annotationContext.entrezID.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsUniprotID(symbolP, entrezIDP, ensemblIDP):
                partialMethods = []
                if symbolP is not None:
                    partialMethods.append(partial(self.annotationContext.uniprotID.GetBySymbol, symbolP))

                if entrezIDP is not None:
                    partialMethods.append(partial(self.annotationContext.uniprotID.GetByEntrezID, entrezIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(self.annotationContext.uniprotID.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsEnsemblID(symbolP, entrezIDP, uniprotIDP):
                partialMethods = []
                if symbolP is not None:
                    partialMethods.append(partial(self.annotationContext.ensemblID.GetBySymbol, symbolP))

                if entrezIDP is not None:
                    partialMethods.append(partial(self.annotationContext.ensemblID.GetByEntrezID, entrezIDP))

                if uniprotIDP is not None:
                    partialMethods.append(partial(self.annotationContext.ensemblID.GetByUniProtID, uniprotIDP))

                return partialMethods

            # Phase II
            # Symbol, EntrezID, UniprotID, EnsemblID
            if symbol is not None or entrezID is not None or uniprotID is not None or ensemblID is not None:
                ordersOfSearch = list(permutations(noneAttributes))
                stopSearch = False
                for orderOfSearch in ordersOfSearch:
                    for attribute in orderOfSearch:
                        if symbol is None and attribute is Attribute.SYMBOL:
                            symbol = GetAttribute(
                                partialGetMethodsSymbol(PreprocessAttribute(entrezID), PreprocessAttribute(uniprotID),
                                                        PreprocessAttribute(ensemblID)))
                        elif entrezID is None and attribute is Attribute.ENTREZ_ID:
                            entrezID = GetAttribute(
                                partialGetMethodsEntrezID(PreprocessAttribute(symbol), PreprocessAttribute(uniprotID),
                                                          PreprocessAttribute(ensemblID)))
                        elif uniprotID is None and attribute is Attribute.UNIPROT_ID:
                            uniprotID = GetAttribute(
                                partialGetMethodsUniprotID(PreprocessAttribute(symbol), PreprocessAttribute(entrezID),
                                                           PreprocessAttribute(ensemblID)))
                        elif ensemblID is None and attribute is Attribute.ENSEMBL_ID:
                            ensemblID = GetAttribute(
                                partialGetMethodsEnsemblID(PreprocessAttribute(symbol), PreprocessAttribute(entrezID),
                                                           PreprocessAttribute(uniprotID)))

                        if symbol is not None and entrezID is not None and uniprotID is not None and \
                                ensemblID is not None:
                            stopSearch = True
                            break

                    if stopSearch:
                        break

            # Phase III
            # Disease Name and DOID(only for OMIM) for HPO
            if source is Source.HPO:
                if term.orpha is not None:
                    diseaseName = self.annotationContext.diseaseName.GetByOrpha(term.orpha)
                elif term.omim is not None:
                    diseaseNameForSearch = "OMIM:" + term.omim
                    doid, doidSource = self.annotationContext.doid.GetByDiseaseNameUsingSearchEngine(
                        diseaseNameForSearch)
                    diseaseName = self.annotationContext.diseaseName.GetByDoid(doid)

                    if doid is None:
                        _doidAndDiseaseNames = self.annotationContext.diseaseName.GetByOmimDoidAndDiseaseName(term.omim)
                        for _doid, _diseaseName in _doidAndDiseaseNames:
                            if _doid is None and _diseaseName is not None:
                                _doid, _doidSource = self.annotationContext.doid. \
                                    GetByDiseaseNameUsingSearchEngine(_diseaseName)
                                doidAndDiseaseNames.append((_doid, _doidSource, _diseaseName))
                            elif _doid is not None:
                                doidAndDiseaseNames.append((_doid, DOID_SOURCE_XREF_OMIM, _diseaseName))

            # DOID
            # Get Doid using xref UMLS
            if (source is Source.DISGENET or source is Source.CLINVAR) and term.umls is not None and doid is None:
                doid, doidSource = self.annotationContext.doid.GetByUmls(term.umls)

            # Get Doid using xref OMIM
            if (source is Source.HUMSAVAR or source is Source.CLINVAR) and term.omim is not None and doid is None:
                doid, doidSource = self.annotationContext.doid.GetByOmim(term.omim)
                if doid is None:
                    diseaseNameForSearch = "OMIM:" + term.omim
                    doid, doidSource = self.annotationContext.doid.GetByDiseaseNameUsingSearchEngine(
                        diseaseNameForSearch)

            # Get Doid using xref ORPHA
            if (source is Source.ORPHANET or source is Source.HPO) and term.orpha is not None and doid is None:
                # Exact xref search
                exactXrefs = self.annotationContext.xrefs.GetByOrphaExact(term.orpha)
                for xref, values in exactXrefs.items():
                    for value in values:
                        doid, doidSource = self.annotationContext.doid.GetByXref(xref, value)
                        if doid is not None:
                            break
                    if doid is not None:
                        break

                # Disease name without search engine
                if doid is None and diseaseName is not None:
                    doid, doidSource = self.annotationContext.doid.GetByDiseaseName(diseaseName)

                preprocessedDiseaesName = PreprocessingDiseaseName(diseaseName, True)
                # BTNT xref search
                if doid is None:
                    maxJaccardIndex = -1
                    btntXrefs = self.annotationContext.xrefs.GetByOrphaBtnt(term.orpha)
                    for xref, values in btntXrefs.items():
                        for value in values:
                            btntDoid, btntDoidSource = self.annotationContext.doid.GetByXref(xref, value)
                            parentDoids = self.annotationContext.diseaseName.GetParentDoidAndDiseaseNamesByDoid(
                                btntDoid)
                            if preprocessedDiseaesName is not None and btntDoid is not None:
                                for parentDoid in parentDoids:
                                    parentDiseaseName = PreprocessingDiseaseName(parentDoid[1], True)
                                    currentJaccardIndex = JaccardSimilarity(parentDiseaseName, preprocessedDiseaesName)
                                    if currentJaccardIndex > maxJaccardIndex:
                                        maxJaccardIndex = currentJaccardIndex
                                        doid = parentDoid[0]
                                        doidSource = btntDoidSource
                            elif preprocessedDiseaesName is None and btntDoid is not None:
                                doid = parentDoids[0][0]
                                if doid is not None:
                                    doidSource = btntDoidSource
                                    break
                        if preprocessedDiseaesName is None and doid is not None:
                            break

                # NTBT xref search
                if doid is None:
                    maxJaccardIndex = -1
                    ntbtXrefs = self.annotationContext.xrefs.GetByOrphaNtbt(term.orpha)
                    for xref, values in ntbtXrefs.items():
                        for value in values:
                            ntbtDoid, ntbtDoidSource = self.annotationContext.doid.GetByXref(xref, value)
                            if preprocessedDiseaesName is not None and ntbtDoid is not None:
                                ntbtDiseaseName = PreprocessingDiseaseName(
                                    self.annotationContext.diseaseName.GetByDoid(ntbtDoid), True)
                                if ntbtDiseaseName is not None:
                                    currentJaccardIndex = JaccardSimilarity(ntbtDiseaseName, preprocessedDiseaesName)
                                    if currentJaccardIndex > maxJaccardIndex:
                                        maxJaccardIndex = currentJaccardIndex
                                        doid = ntbtDoid
                                        doidSource = ntbtDoidSource
                                else:
                                    doid = ntbtDoid
                                    doidSource = ntbtDoidSource
                            elif preprocessedDiseaesName is None and ntbtDoid is not None:
                                doid = ntbtDoid
                                doidSource = ntbtDoidSource
                                break
                        if preprocessedDiseaesName is None and doid is not None:
                            break

                # Other xref search
                if doid is None:
                    maxJaccardIndex = -1
                    otherXrefs = self.annotationContext.xrefs.GetByOrphaOther(term.orpha)
                    for xref, values in otherXrefs.items():
                        for value in values:
                            otherDoid, otherDoidSource = self.annotationContext.doid.GetByXref(xref, value)
                            if preprocessedDiseaesName is not None and otherDoid is not None:
                                otherDiseaseName = PreprocessingDiseaseName(
                                    self.annotationContext.diseaseName.GetByDoid(otherDoid), True)
                                if otherDiseaseName is not None:
                                    currentJaccardIndex = JaccardSimilarity(otherDiseaseName, preprocessedDiseaesName)
                                    if currentJaccardIndex > maxJaccardIndex:
                                        maxJaccardIndex = currentJaccardIndex
                                        doid = otherDoid
                                        doidSource = otherDoidSource
                                else:
                                    doid = otherDoid
                                    doidSource = otherDoidSource
                            elif preprocessedDiseaesName is None and otherDoid is not None:
                                doid = otherDoid
                                doidSource = otherDoidSource
                                break
                        if preprocessedDiseaesName is None and doid is not None:
                            break

            # Get Doid using disease name
            if doid is None:
                doid, doidSource = self.annotationContext.doid.GetByDiseaseNameUsingSearchEngine(diseaseName)

            # Disease Name
            if diseaseName is None and doid is not None:
                diseaseName = self.annotationContext.diseaseName.GetByDoid(doid)

            # Phase IV
            if source is Source.HPO:
                if doidAndDiseaseNames:
                    for doid, doidSource, diseaseName in doidAndDiseaseNames:
                        if doid is None and diseaseName is None and term.omim is not None:
                            sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName,
                                                              "<OMIM>" + term.omim, doidSource))
                        elif doid is not None or diseaseName is not None:
                            sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName,
                                                              diseaseName, doidSource))
                elif doid is None and diseaseName is None and (term.omim is not None or term.orpha is not None):
                    changedDiseaseName = "<OMIM>" + term.omim if term.omim is not None else "<ORPHA>" + term.orpha
                    sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName,
                                                      changedDiseaseName, doidSource))
                elif doid is not None or diseaseName is not None:
                    sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName,
                                                      diseaseName, doidSource))
            elif source is Source.DISEASES and term.ensemblProteinID is not None and \
                    symbol is None and entrezID is None and ensemblID is None and uniprotID is None:
                sourceSet.add(AnnotationRowOutput("<PROTEIN_ID>" + term.ensemblProteinID, entrezID, uniprotID,
                                                  ensemblID, doid, sourceName, diseaseName, doidSource))
            else:
                sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName, diseaseName,
                                                  doidSource))

            if progress is not None:
                progress.increase_step()

        return source, sourceSet

    def __ParseSources(self, progress):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(),
                      TaskProgressColumn(), MofNCompleteColumn(),
                      TimeElapsedColumn(), TimeRemainingColumn()) as progressBar:
            with ThreadPoolExecutor() as executor:
                progressTask = progressBar.add_task("Parsing", total=self.dbContext.GetTotalParsingLength())
                for source, sourceSet in executor.map(lambda args: self.__ParseSource(*args),
                                                      [(source, progress, progressBar, progressTask)
                                                       for source in self.__sources]):
                    self.__sourcesAnnotationSetDict[source] = sourceSet

    def __CreateFullAnnotationSet(self):
        for source in self.__sources:
            self.__annotationSet |= self.__sourcesAnnotationSetDict[source]

    def GetAnnotationSet(self):
        return self.__annotationSet

    def GetAnnotationSetDict(self):
        return self.__sourcesAnnotationSetDict

    def CreateAnnotationFile(self, filePath):
        WriteStructureToFile(filePath, sorted(self.__annotationSet, key=lambda term: term.source),
                             ANNOTATION_FILE_HEADER)
