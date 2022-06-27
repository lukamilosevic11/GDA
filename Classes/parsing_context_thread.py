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

from Classes.annotation_context import AnnotationContext
from Classes.annotation_row import AnnotationRowOutput
from Classes.db_context import DBContext
from Common.constants import DOID_SOURCE_DATABASE, ANNOTATION_FILE_HEADER, DOID_SOURCE_XREF_OMIM
from Common.init import Source, partial, Attribute, permutations, ThreadPoolExecutor, Progress, SpinnerColumn, \
    TimeElapsedColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn
from Common.util import GetAttribute, WriteStructureToFile, JaccardSimilarity, PreprocessingDiseaseName


class ParsingContextThread:
    def __init__(self, progress, createCollection=False):
        self.dbContext = DBContext()
        self.__totalLength = self.dbContext.GetTotalParsingLength()
        self.annotationContext = AnnotationContext(self.dbContext, createCollection)
        self.__sources = Source.GetSourcesForParsing()
        self.__sourcesAnnotationSetDict = {}
        self.__annotationSet = set()
        self.__ParseSources(progress)
        self.__CreateFullAnnotationSet()

    def __ParseSource(self, source, progress, progressBar, parsingTask):
        sourceSet = set()
        sourceName = Source.GetSourceName(source)
        sourceDB = self.dbContext.GetDatabaseBySource(source)
        sourceTask = progressBar.add_task(sourceName, total=len(sourceDB))
        for term in sourceDB:
            progressBar.update(parsingTask, advance=1)
            progressBar.update(sourceTask, advance=1)
            symbol = term.symbol
            entrezID = term.entrezID
            uniprotID = term.uniprotID
            ensemblID = term.ensemblID
            doid = term.doid
            diseaseName = term.diseaseName
            doidSource = DOID_SOURCE_DATABASE if source is Source.DISEASES and doid is not None else None
            multipleHPORowsFlag = False
            doidAndDiseaseNames = None

            noneAttributes = []
            entrezIDFlagNone = False
            uniprotIDFlagNone = False
            ensemblIDFlagNone = False
            if entrezID is None:
                noneAttributes.append(Attribute.ENTREZ_ID)
                entrezIDFlagNone = True
            if uniprotID is None:
                noneAttributes.append(Attribute.UNIPROT_ID)
                uniprotIDFlagNone = True
            if ensemblID is None:
                noneAttributes.append(Attribute.ENSEMBL_ID)
                ensemblIDFlagNone = True

            foundAttributes = {
                Attribute.ENTREZ_ID: not entrezIDFlagNone,
                Attribute.UNIPROT_ID: not uniprotIDFlagNone,
                Attribute.ENSEMBL_ID: not ensemblIDFlagNone
            }

            def partialGetMethodsEntrezID(symbolP, uniprotIDP, ensemblIDP):
                partialMethods = [partial(self.annotationContext.entrezID.GetBySymbol, symbolP)]
                if uniprotIDP is not None:
                    partialMethods.append(partial(self.annotationContext.entrezID.GetByUniprotID, uniprotIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(self.annotationContext.entrezID.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsUniprotID(symbolP, entrezIDP, ensemblIDP):
                partialMethods = [partial(self.annotationContext.uniprotID.GetBySymbol, symbolP)]
                if entrezIDP is not None:
                    partialMethods.append(partial(self.annotationContext.uniprotID.GetByEntrezID, entrezIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(self.annotationContext.uniprotID.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsEnsemblID(symbolP, entrezIDP, uniprotIDP):
                partialMethods = [partial(self.annotationContext.ensemblID.GetBySymbol, symbolP)]
                if entrezIDP is not None:
                    partialMethods.append(partial(self.annotationContext.ensemblID.GetByEntrezID, entrezIDP))

                if uniprotIDP is not None:
                    partialMethods.append(partial(self.annotationContext.ensemblID.GetByUniprotID, uniprotIDP))

                return partialMethods

            # EntrezID, UniprotID, EnsemblID
            ordersOfSearch = list(permutations(noneAttributes))
            stopSearch = False
            for order in ordersOfSearch:
                for attribute in order:
                    if entrezID is None and attribute is Attribute.ENTREZ_ID:
                        entrezID = GetAttribute(partialGetMethodsEntrezID(symbol, ensemblID, uniprotID))
                        if entrezID is not None:
                            foundAttributes[attribute] = True
                    elif uniprotID is None and attribute is Attribute.UNIPROT_ID:
                        uniprotID = GetAttribute(partialGetMethodsUniprotID(symbol, entrezID, ensemblID))
                        if uniprotID is not None:
                            foundAttributes[attribute] = True
                    elif ensemblID is None and attribute is Attribute.ENSEMBL_ID:
                        ensemblID = GetAttribute(partialGetMethodsEnsemblID(symbol, entrezID, uniprotID))
                        if ensemblID is not None:
                            foundAttributes[attribute] = True

                    if foundAttributes[Attribute.ENTREZ_ID] and foundAttributes[Attribute.UNIPROT_ID] and \
                            foundAttributes[Attribute.ENSEMBL_ID]:
                        stopSearch = True
                        break
                if stopSearch:
                    break

            # Disease Name and DOID(only for OMIM) for HPO
            if source is Source.HPO:
                if term.orpha is not None:
                    diseaseName = self.annotationContext.diseaseName.GetByOrpha(term.orpha)
                elif term.omim is not None and doid is None:
                    doidAndDiseaseNames = self.annotationContext.diseaseName.GetByOmimDoidAndDiseaseName(term.omim)
                    if len(doidAndDiseaseNames) == 1:
                        doid, diseaseName = doidAndDiseaseNames[0]
                        if doid is not None:
                            doidSource = DOID_SOURCE_XREF_OMIM
                    elif len(doidAndDiseaseNames) > 1:
                        multipleHPORowsFlag = True

                    if doid is None:
                        diseaseNameForSearch = "OMIM:" + term.omim
                        doid, doidSource = self.annotationContext.doid.GetByDiseaseName(diseaseNameForSearch)
                        diseaseName = self.annotationContext.diseaseName.GetByDoid(doid)
                        if diseaseName is not None and doid is not None:
                            multipleHPORowsFlag = False

            # DOID
            # Get Doid using xref UMLS
            if (source is Source.DISGENET or source is Source.CLINVAR) and term.umls is not None and doid is None:
                doid, doidSource = self.annotationContext.doid.GetByUmls(term.umls)

            # Get Doid using xref OMIM
            if (source is Source.HUMSAVAR or source is Source.CLINVAR) and term.omim is not None and doid is None:
                doid, doidSource = self.annotationContext.doid.GetByOmim(term.omim)
                if doid is None:
                    diseaseNameForSearch = "OMIM:" + term.omim
                    doid, doidSource = self.annotationContext.doid.GetByDiseaseName(diseaseNameForSearch)

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
                if doid is None:
                    doid, doidSource = self.annotationContext.doid.GetByDiseaseNameWithoutSearchEngine(diseaseName)

                preprocessedDiseaesName = PreprocessingDiseaseName(diseaseName, True)
                # BTNT xref search
                if doid is None:
                    maxJaccardIndex = -1
                    btntXrefs = self.annotationContext.xrefs.GetByOrphaBtnt(term.orpha)
                    for xref, values in btntXrefs.items():
                        for value in values:
                            btntDoid, btntDoidSource = self.annotationContext.doid.GetByXref(xref, value)
                            parentDoids = self.annotationContext.diseaseName.GetParentDoidAndDiseaseNamesByDoid(btntDoid)
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
                                ntbtDiseaseName = \
                                    PreprocessingDiseaseName(self.annotationContext.diseaseName.GetByDoid(ntbtDoid), True)
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
                                otherDiseaseName = \
                                    PreprocessingDiseaseName(self.annotationContext.diseaseName.GetByDoid(otherDoid),
                                                             True)
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
                doid, doidSource = self.annotationContext.doid.GetByDiseaseName(diseaseName)

            # Disease Name
            if diseaseName is None and doid is not None:
                diseaseName = self.annotationContext.diseaseName.GetByDoid(doid)

            if multipleHPORowsFlag and (doid is None or diseaseName is None) and doidAndDiseaseNames is not None:
                doidSource = DOID_SOURCE_XREF_OMIM
                for doid, diseaseName in doidAndDiseaseNames:
                    sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName,
                                                      diseaseName, doidSource))
            else:
                sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName, diseaseName,
                                                  doidSource))

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
