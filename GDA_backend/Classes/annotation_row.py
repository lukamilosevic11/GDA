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


class AnnotationRow:
    def __init__(self, symbol, entrezID, uniprotID, ensemblID, doid, source, diseaseName):
        self.symbol = symbol
        self.entrezID = entrezID
        self.uniprotID = uniprotID
        self.ensemblID = ensemblID
        self.doid = doid
        self.source = source
        self.diseaseName = diseaseName

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                other.symbol == self.symbol and
                other.entrezID == self.entrezID and
                other.uniprotID == self.uniprotID and
                other.ensemblID == self.ensemblID and
                other.doid == self.doid and
                other.source == self.source and
                other.diseaseName == self.diseaseName)

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.uniprotID, self.ensemblID, self.doid, self.source,
                     self.diseaseName))

    def __str__(self):
        return str(self.symbol) + '\t' + \
               str(self.entrezID) + '\t' + \
               str(self.uniprotID) + '\t' + \
               str(self.ensemblID) + '\t' + \
               str(self.doid) + '\t' + \
               str(self.source) + '\t' + \
               str(self.diseaseName)


class AnnotationRowOutput(AnnotationRow):
    def __init__(self, symbol, entrezID, uniprotID, ensemblID, doid, source, diseaseName, doidSource):
        super(AnnotationRowOutput, self).__init__(symbol, entrezID, uniprotID, ensemblID, doid, source, diseaseName)
        self.doidSource = doidSource

    def __eq__(self, other):
        return super(AnnotationRowOutput, self).__eq__(other) and self.doidSource == other.doidSource

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.uniprotID, self.ensemblID, self.doid, self.diseaseName,
                     self.doidSource))

    def __str__(self):
        return super(AnnotationRowOutput, self).__str__() + '\t' + str(self.doidSource)


class ClinVarRow(AnnotationRow):
    def __init__(self, symbol, entrezID, diseaseName, umls, omim):
        super(ClinVarRow, self).__init__(symbol, entrezID, None, None, None, "ClinVar", diseaseName)
        self.umls = umls
        self.omim = omim

    def __eq__(self, other):
        return super(ClinVarRow, self).__eq__(other) and self.umls == other.umls and self.omim == other.omim

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.diseaseName, self.umls, self.omim))

    def __str__(self):
        return super(ClinVarRow, self).__str__() + '\t' + str(self.umls) + '\t' + str(self.omim)


class CosmicRow(AnnotationRow):
    def __init__(self, symbol, entrezID, diseaseName):
        super(CosmicRow, self).__init__(symbol, entrezID, None, None, None, "Cosmic", diseaseName)


class DiseasesRow(AnnotationRow):
    def __init__(self, symbol, doid, diseaseName):
        super(DiseasesRow, self).__init__(symbol, None, None, None, doid, "Diseases", diseaseName)


class DisGeNetRow(AnnotationRow):
    def __init__(self, symbol, entrezID, diseaseName, umls):
        super(DisGeNetRow, self).__init__(symbol, entrezID, None, None, None, "DisGeNet", diseaseName)
        self.umls = umls

    def __eq__(self, other):
        return super(DisGeNetRow, self).__eq__(other) and self.umls == other.umls

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.diseaseName, self.umls))

    def __str__(self):
        return super(DisGeNetRow, self).__str__() + '\t' + str(self.umls)


class HPORow(AnnotationRow):
    def __init__(self, symbol, entrezID, omim, orpha):
        super(HPORow, self).__init__(symbol, entrezID, None, None, None, "HPO", None)
        self.omim = omim
        self.orpha = orpha

    def __eq__(self, other):
        return super(HPORow, self).__eq__(other) and self.omim == other.omim and self.orpha == other.orpha

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.omim, self.orpha))

    def __str__(self):
        return super(HPORow, self).__str__() + '\t' + str(self.omim) + '\t' + str(self.orpha)


class HumsaVarRow(AnnotationRow):
    def __init__(self, symbol, uniprotID, diseaseName, omim):
        super(HumsaVarRow, self).__init__(symbol, None, uniprotID, None, None, "HumsaVar", diseaseName)
        self.omim = omim

    def __eq__(self, other):
        return super(HumsaVarRow, self).__eq__(other) and self.omim == other.omim

    def __hash__(self):
        return hash((self.symbol, self.uniprotID, self.diseaseName, self.omim))

    def __str__(self):
        return super(HumsaVarRow, self).__str__() + '\t' + str(self.omim)


class OrphanetRow(AnnotationRow):
    def __init__(self, symbol, uniprotID, ensemblID, diseaseName, orpha):
        super(OrphanetRow, self).__init__(symbol, None, uniprotID, ensemblID, None, "Orphanet", diseaseName)
        self.orpha = orpha

    def __eq__(self, other):
        return super(OrphanetRow, self).__eq__(other) and self.orpha == other.orpha

    def __hash__(self):
        return hash((self.symbol, self.uniprotID, self.ensemblID, self.diseaseName, self.orpha))

    def __str__(self):
        return super(OrphanetRow, self).__str__() + '\t' + str(self.orpha)


class OrphanetXrefRow:
    def __init__(self, orpha, eDict, btntDict, ntbtDict, otherDict, diseaseName):
        self.orpha = orpha
        self.__eDict = eDict
        self.__btntDict = btntDict
        self.__ntbtDict = ntbtDict
        self.__otherDict = otherDict
        self.diseaseName = diseaseName

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.orpha == other.orpha and self.__eDict == other.__eDict and \
               self.__btntDict == other.__btntDict and self.__ntbtDict == other.__ntbtDict and \
               self.__otherDict == other.__otherDict and self.diseaseName == other.diseaseName

    def __hash__(self):
        return hash((self.orpha, self.diseaseName))

    def __str__(self):
        return str(self.orpha) + '\t' + str(self.diseaseName)

    def GetExactXrefs(self):
        return self.__eDict

    def GetBtntXrefs(self):
        return self.__btntDict

    def GetNtbtXrefs(self):
        return self.__ntbtDict

    def GetOtherXrefs(self):
        return self.__otherDict


class OBORow(AnnotationRow):
    def __init__(self, doid, diseaseName, synonyms, parentDoids, xrefs, altIds, definition):
        super(OBORow, self).__init__(None, None, None, None, doid, "Obo", diseaseName)
        self.definition = definition
        self.__synonyms = synonyms
        self.__parentDoids = parentDoids
        self.__xrefs = xrefs
        self.__altIds = altIds

    def __eq__(self, other):
        return super(OBORow, self).__eq__(other) and self.__synonyms == other.__synonyms \
               and self.__parentDoids == other.__parentDoids and self.__xrefs == other.__xrefs \
               and self.__altIds == other.__altIds

    def __hash__(self):
        return hash((self.doid, self.diseaseName))

    def __str__(self):
        synonymsStr = '  '.join(self.GetSynonyms()).strip()
        parentDoidsStr = '  '.join(self.GetParentDiseaseNames()).strip()

        if len(synonymsStr) != 0:
            synonymsStr = "\n\tSynonyms: " + synonymsStr

        if len(parentDoidsStr) != 0:
            parentDoidsStr = "\n\tParent Doids: " + parentDoidsStr

        return super(OBORow, self).__str__() + synonymsStr + parentDoidsStr

    def GetSynonyms(self):
        return [synonym.description.strip() for synonym in self.__synonyms]

    def GetParentDiseaseNames(self):
        return [parentDoid.name.strip() for parentDoid in self.__parentDoids]

    def GetParentDiseaseNameAndDoids(self):
        return [(parentDoid.id.strip(), parentDoid.name.strip()) for parentDoid in self.__parentDoids]

    def GetXrefs(self):
        return self.__xrefs

    def GetAlternateIds(self):
        return self.__altIds


class UniprotRow(AnnotationRow):
    def __init__(self, symbol, symbolSynonyms, entrezID, ensemblID, uniprotID):
        super(UniprotRow, self).__init__(symbol, entrezID, uniprotID, ensemblID, None, "Uniprot", None)
        self.__symbolSynonyms = symbolSynonyms

    def __eq__(self, other):
        return super(UniprotRow, self).__eq__(other) and self.__symbolSynonyms == other.__symbolSynonyms

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.ensemblID, self.uniprotID))

    def __str__(self):
        symbolSynonymsStr = '  '.join(self.getSymbolSynonyms()).strip()

        if len(symbolSynonymsStr) != 0:
            symbolSynonymsStr = "\n\tSymbol Synonyms: " + symbolSynonymsStr

        return super(UniprotRow, self).__str__() + symbolSynonymsStr

    def getSymbolSynonyms(self):
        return [symbolSynonym for symbolSynonym in self.__symbolSynonyms]


class HugoRow(AnnotationRow):
    def __init__(self, symbol, entrezID, uniprotID, ensemblID, uniprotIDs, aliasSymbols):
        super(HugoRow, self).__init__(symbol, entrezID, uniprotID, ensemblID, None, "Hugo", None)
        self.__uniprotIDs = uniprotIDs
        self.__aliasSymbols = aliasSymbols

    def __eq__(self, other):
        return super(HugoRow, self).__eq__(
            other) and self.__uniprotIDs == other.__uniprotIDs and self.__aliasSymbols == other.__aliasSymbols

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.uniprotID, self.ensemblID))

    def __str__(self):
        uniprotIDsStr = '  '.join(self.getUniprotIDs()).strip()
        aliasSymbolsStr = '  '.join(self.getSymbolSynonyms()).strip()

        if len(uniprotIDsStr) != 0:
            uniprotIDsStr = "\n\tUniprot IDs: " + uniprotIDsStr

        if len(aliasSymbolsStr) != 0:
            aliasSymbolsStr = "\n\tAlias Symbols IDs: " + aliasSymbolsStr

        return super(HugoRow, self).__str__() + uniprotIDsStr + aliasSymbolsStr

    def getUniprotIDs(self):
        return [uniprotID for uniprotID in self.__uniprotIDs]

    def getSymbolSynonyms(self):
        return [symbolSynonym for symbolSynonym in self.__aliasSymbols]
