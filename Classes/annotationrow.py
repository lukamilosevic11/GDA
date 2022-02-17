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
                other.diseaseName == self.diseaseName)

    def __hash__(self):
        return hash((self.symbol, self.entrezID, self.uniprotID, self.ensemblID, self.doid, self.diseaseName))

    def __str__(self):
        return str(self.symbol) + '\t' + \
               str(self.entrezID) + '\t' + \
               str(self.uniprotID) + '\t' + \
               str(self.ensemblID) + '\t' + \
               str(self.doid) + '\t' + \
               str(self.source) + '\t' + \
               str(self.diseaseName)


class ClinVarRow(AnnotationRow):
    def __init__(self, symbol, entrezID, diseaseName):
        super(ClinVarRow, self).__init__(symbol, entrezID, None, None, None, "ClinVar", diseaseName)


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
        return super(DisGeNetRow, self).__str__() + "\t" + str(self.umls)


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


class HugoRow(AnnotationRow):
    def __init__(self, symbol, ensemblID):
        super(HugoRow, self).__init__(symbol, None, None, ensemblID, None, "Hugo", None)


class HumsaVarRow(AnnotationRow):
    def __init__(self, symbol, diseaseName, omim):
        super(HumsaVarRow, self).__init__(symbol, None, None, None, None, "HumsaVar", diseaseName)
        self.omim = omim

    def __eq__(self, other):
        return super(HumsaVarRow, self).__eq__(other) and self.omim == other.omim

    def __hash__(self):
        return hash((self.symbol, self.diseaseName, self.omim))

    def __str__(self):
        return super(HumsaVarRow, self).__str__() + '\t' + str(self.omim)


class OBORow(AnnotationRow):
    def __init__(self, doid, diseaseName, synonyms, parentDoids):
        self.synonyms = synonyms
        self.parentDoids = parentDoids
        super(OBORow, self).__init__(None, None, None, None, doid, "Obo", diseaseName)


class OrphanetRow(AnnotationRow):
    def __init__(self, symbol, ensemblID, diseaseName):
        super(OrphanetRow, self).__init__(symbol, None, None, ensemblID, None, "Orphanet", diseaseName)


class UniprotRow(AnnotationRow):
    def __init__(self, symbol, entrezID, uniprotID):
        super(UniprotRow, self).__init__(symbol, entrezID, uniprotID, None, None, "Uniprot", None)
