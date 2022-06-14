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
from Common.constants import MAX_JACCARD_INDEX
from Common.init import Source, partial, Thread, Lock, Attribute, permutations
from Common.util import GetAttribute, WriteStructureToFile, JaccardSimilarity


class ParsingContextThread:
    def __init__(self, dropCollection=False):
        self.dbContext = DBContext()
        self.__totalLength = self.dbContext.GetTotalLength()
        self.annotationContext = AnnotationContext(self.dbContext, dropCollection)
        self.__sources = Source.GetSourcesForParsing()
        self.__sourcesAnnotationSetDict = {}
        self.__annotationSet = set()
        self.__ParseSources()
        self.__CreateFullAnnotationSet()

    def __ParseSource(self, source, sourceName, sourceDB, lock,
                      entrezIDAttribute,
                      uniprotIDAttribute,
                      ensemblIDAttribute,
                      doidAttribute,
                      diseaseNameAttribute,
                      xrefsAttribute):
        sourceSet = set()
        for term in sourceDB:
            symbol = term.symbol
            entrezID = term.entrezID
            uniprotID = term.uniprotID
            ensemblID = term.ensemblID
            doid = term.doid
            diseaseName = term.diseaseName
            jaccardIndex = None if sourceName != "Diseases" else str(MAX_JACCARD_INDEX)

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
                partialMethods = [partial(entrezIDAttribute.GetBySymbol, symbolP)]
                if uniprotIDP is not None:
                    partialMethods.append(partial(entrezIDAttribute.GetByUniprotID, uniprotIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(entrezIDAttribute.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsUniprotID(symbolP, entrezIDP, ensemblIDP):
                partialMethods = [partial(uniprotIDAttribute.GetBySymbol, symbolP)]
                if entrezIDP is not None:
                    partialMethods.append(partial(uniprotIDAttribute.GetByEntrezID, entrezIDP))

                if ensemblIDP is not None:
                    partialMethods.append(partial(uniprotIDAttribute.GetByEnsemblID, ensemblIDP))

                return partialMethods

            def partialGetMethodsEnsemblID(symbolP, entrezIDP, uniprotIDP):
                partialMethods = [partial(ensemblIDAttribute.GetBySymbol, symbolP)]
                if entrezIDP is not None:
                    partialMethods.append(partial(ensemblIDAttribute.GetByEntrezID, entrezIDP))

                if uniprotIDP is not None:
                    partialMethods.append(partial(ensemblIDAttribute.GetByUniprotID, uniprotIDP))

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

            # Disease Name for HPO
            if source is Source.HPO:
                if term.orpha is not None:
                    diseaseName = diseaseNameAttribute.GetByOrpha(term.orpha)
                elif term.omim is not None:
                    diseaseNames = diseaseNameAttribute.GetByOmim(term.omim)
                    if len(diseaseNames) == 1:
                        diseaseName = diseaseNames[0]
                        # elif len(diseaseNames) > 1:
                        #     print(term.omim, diseaseNames)  # TODO: remove
                        # else:
                        diseaseNameForSearch = "OMIM:" + term.omim
                        # print(term.omim)  # TODO: remove
                        # pass  # TODO: Notify which omim has different disease names

            # DOID
            # Get Doid using xref UMLS
            if (source is Source.DISGENET or source is Source.CLINVAR) and term.umls is not None and doid is None:
                doid, jaccardIndex = doidAttribute.GetByUmls(term.umls)

            # Get Doid using xref OMIM
            if (source is Source.HUMSAVAR or source is Source.HPO or source is Source.CLINVAR) \
                    and term.omim is not None and doid is None:
                doid, jaccardIndex = doidAttribute.GetByOmim(term.omim)
                if doid is None:
                    diseaseNameForSearch = "OMIM:" + term.omim
                    doid, jaccardIndex = doidAttribute.GetByDiseaseName(diseaseNameForSearch)

            # Get Doid using xref ORPHA
            if (source is Source.ORPHANET or source is Source.HPO) and term.orpha is not None and doid is None:
                # Exact xref search
                exactXrefs = xrefsAttribute.GetByOrphaExact(term.orpha)
                for xref, value in exactXrefs.items():
                    doid, jaccardIndex = doidAttribute.GetByXref(xref, value)
                    if doid is not None:
                        break

                # Disease name without search engine and not exact xref search
                if doid is None:
                    # Disease name without search engine
                    doid, jaccardIndex = doidAttribute.GetByDiseaseNameWithoutSearchEngine(diseaseName)

                    # Not exact xref search
                    if doid is None:
                        notExactXrefs = xrefsAttribute.GetByOrphaNotExact(term.orpha)
                        for xref, value in notExactXrefs.items():
                            doid, jaccardIndex = doidAttribute.GetByXref(xref, value)
                            if doid is not None:
                                print(diseaseName + " *** " + diseaseNameAttribute.GetByDoid(doid), doid)
                                print(JaccardSimilarity(diseaseName, diseaseNameAttribute.GetByDoid(doid)))  # TODO: REMOVE
                                break

            # Get Doid using disease name
            if doid is None:
                doid, jaccardIndex = doidAttribute.GetByDiseaseName(diseaseName)

            # Disease Name
            if diseaseName is None and doid is not None:
                diseaseName = diseaseNameAttribute.GetByDoid(doid)

            sourceSet.add(AnnotationRowOutput(symbol, entrezID, uniprotID, ensemblID, doid, sourceName, diseaseName,
                                              jaccardIndex))
        with lock:
            self.__sourcesAnnotationSetDict[source] = sourceSet

    def __ParseSources(self):
        threads = []
        lock = Lock()
        entrezIDAttribute = self.annotationContext.entrezID
        uniprotIDAttribute = self.annotationContext.uniprotID
        ensemblIDAttribute = self.annotationContext.ensemblID
        doidAttribute = self.annotationContext.doid
        diseaseNameAttribute = self.annotationContext.diseaseName
        xrefsAttribute = self.annotationContext.xrefs

        for source in self.__sources:
            sourceName = Source.GetSourceName(source)
            sourceDB = self.dbContext.GetDatabaseBySource(source)
            t = Thread(target=self.__ParseSource, args=(source, sourceName, sourceDB, lock,
                                                        entrezIDAttribute,
                                                        uniprotIDAttribute,
                                                        ensemblIDAttribute,
                                                        doidAttribute,
                                                        diseaseNameAttribute,
                                                        xrefsAttribute))
            threads.append(t)
            t.start()

        for th in threads:
            th.join()

    def __CreateFullAnnotationSet(self):
        for source in self.__sources:
            self.__annotationSet |= self.__sourcesAnnotationSetDict[source]

    def GetAnnotationSet(self):
        return self.__annotationSet

    def GetAnnotationSetDict(self):
        return self.__sourcesAnnotationSetDict

    def CreateAnnotationFile(self, filePath):
        WriteStructureToFile(filePath, sorted(self.__annotationSet, key=lambda term: term.source))
