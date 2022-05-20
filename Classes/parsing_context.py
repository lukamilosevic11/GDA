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
from Classes.annotation_row import AnnotationRow
from Classes.db_context import DBContext
from Common.init import Source, partial
from Common.util import GetAttribute, WriteStructureToFile


class ParsingContext:
    def __init__(self, dropCollection=False):
        self.dbContext = DBContext()
        self.annotationContext = AnnotationContext(self.dbContext, dropCollection)
        self.__sources = Source.GetSourcesForParsing()
        self.__sourcesAnnotationSetDict = {}
        self.__annotationSet = set()
        self.__ParseSources()
        self.__CreateFullAnnotationSet()

    def __ParseSources(self):
        entrezIDAttribute = self.annotationContext.entrezID
        uniprotIDAttribute = self.annotationContext.uniprotID
        ensemblIDAttribute = self.annotationContext.ensemblID
        doidAttribute = self.annotationContext.doid
        diseaseNameAttribute = self.annotationContext.diseaseName

        for source in self.__sources:
            sourceSet = set()
            sourceName = Source.GetSourceName(source)
            sourceDB = self.dbContext.GetDatabaseBySource(source)
            for term in sourceDB:
                symbol = term.symbol
                entrezID = term.entrezID
                uniprotID = term.uniprotID
                ensemblID = term.ensemblID
                doid = term.doid
                diseaseName = term.diseaseName

                if entrezID is None:
                    partialGetMethods = [partial(entrezIDAttribute.GetBySymbol, symbol),
                                         partial(entrezIDAttribute.GetByEnsemblID, ensemblID),
                                         partial(entrezIDAttribute.GetByUniprotID, uniprotID)]
                    entrezID = GetAttribute(partialGetMethods)

                if uniprotID is None:
                    partialGetMethods = [partial(uniprotIDAttribute.GetBySymbol, symbol),
                                         partial(uniprotIDAttribute.GetByEntrezID, entrezID),
                                         partial(uniprotIDAttribute.GetByEnsemblID, ensemblID)]
                    uniprotID = GetAttribute(partialGetMethods)

                if ensemblID is None:
                    partialGetMethods = [partial(ensemblIDAttribute.GetBySymbol, symbol),
                                         partial(ensemblIDAttribute.GetByEntrezID, entrezID),
                                         partial(ensemblIDAttribute.GetByUniprotID, uniprotID)]
                    ensemblID = GetAttribute(partialGetMethods)

                if doid is None:
                    partialGetMethods = [partial(doidAttribute.GetByDiseaseName, diseaseName)]
                    doid = GetAttribute(partialGetMethods)

                if diseaseName is None:
                    partialGetMethods = [partial(diseaseNameAttribute.GetBySymbol, symbol),
                                         partial(diseaseNameAttribute.GetByEntrezID, entrezID),
                                         partial(diseaseNameAttribute.GetByEnsemblID, ensemblID),
                                         partial(diseaseNameAttribute.GetByDoid, doid)]
                    diseaseName = GetAttribute(partialGetMethods)

                sourceSet.add(AnnotationRow(symbol, entrezID, uniprotID, ensemblID, doid, sourceName, diseaseName))

            self.__sourcesAnnotationSetDict[source] = sourceSet

    def __CreateFullAnnotationSet(self):
        for source in self.__sources:
            self.__annotationSet |= self.__sourcesAnnotationSetDict[source]

    def GetAnnotationSet(self):
        return self.__annotationSet

    def GetAnnotationSetDict(self):
        return self.__sourcesAnnotationSetDict

    def CreateAnnotationFile(self, filePath):
        WriteStructureToFile(filePath, sorted(self.__annotationSet, key=lambda term: term.source))
