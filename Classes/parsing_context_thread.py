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
from Common.init import Source, partial, Thread, Lock, Attribute, permutations, time
from Common.util import GetAttribute, WriteStructureToFile


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
                      diseaseNameAttribute):
        sourceSet = set()
        for term in sourceDB:
            symbol = term.symbol
            entrezID = term.entrezID
            uniprotID = term.uniprotID
            ensemblID = term.ensemblID
            doid = term.doid
            diseaseName = term.diseaseName
            jaccardIndex = None if sourceName != "Diseases" else "100.0"

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
                Attribute.ENTREZ_ID: entrezIDFlagNone,
                Attribute.UNIPROT_ID: uniprotIDFlagNone,
                Attribute.ENSEMBL_ID: ensemblIDFlagNone
            }

            def partialGetMethodsEntrezID(symbolL, uniprotIDL, ensemblIDL):
                partialMethods = [partial(entrezIDAttribute.GetBySymbol, symbolL)]
                if uniprotIDL is not None:
                    partialMethods.append(partial(entrezIDAttribute.GetByUniprotID, uniprotIDL))

                if ensemblIDL is not None:
                    partialMethods.append(partial(entrezIDAttribute.GetByEnsemblID, ensemblIDL))

                return partialMethods

            def partialGetMethodsUniprotID(symbolL, entrezIDL, ensemblIDL):
                partialMethods = [partial(uniprotIDAttribute.GetBySymbol, symbolL)]
                if entrezIDL is not None:
                    partialMethods.append(partial(uniprotIDAttribute.GetByEntrezID, entrezIDL))

                if ensemblIDL is not None:
                    partialMethods.append(partial(uniprotIDAttribute.GetByEnsemblID, ensemblIDL))

                return partialMethods

            def partialGetMethodsEnsemblID(symbolL, entrezIDL, uniprotIDL):
                partialMethods = [partial(ensemblIDAttribute.GetBySymbol, symbolL)]
                if entrezIDL is not None:
                    partialMethods.append(partial(ensemblIDAttribute.GetByEntrezID, entrezIDL))

                if uniprotIDL is not None:
                    partialMethods.append(partial(ensemblIDAttribute.GetByUniprotID, uniprotIDL))

                return partialMethods

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

            if doid is None and diseaseName is not None:
                doid, jaccardIndex = doidAttribute.GetByDiseaseName(diseaseName)

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

        for source in self.__sources:
            sourceName = Source.GetSourceName(source)
            sourceDB = self.dbContext.GetDatabaseBySource(source)
            t = Thread(target=self.__ParseSource, args=(source, sourceName, sourceDB, lock,
                                                        entrezIDAttribute,
                                                        uniprotIDAttribute,
                                                        ensemblIDAttribute,
                                                        doidAttribute,
                                                        diseaseNameAttribute))
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
