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

from Common.constants import COLLECTION_NAME_DOID, QUERY_BY_DOID, MAX_JACCARD_INDEX
from Common.init import Xref
from Common.util import PreprocessingDiseaseName, JaccardSimilarity


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
    def __init__(self, searchEngineClient, diseaseNameFrozenSetDict, omimDict, umlsDict, meshDict, gardDict, medDraDict,
                 icd10Dict):
        self.__searchEngineClient = searchEngineClient
        self.__diseaseNameFrozenSetDict = diseaseNameFrozenSetDict
        self.__omimDict = omimDict
        self.__umlsDict = umlsDict
        self.__meshDict = meshDict
        self.__gardDict = gardDict
        self.__medDraDict = medDraDict
        self.__icd10Dict = icd10Dict

    def GetByOmim(self, omim):
        return (self.__omimDict[omim], MAX_JACCARD_INDEX) if omim in self.__omimDict else (None, None)

    def GetByUmls(self, umls):
        return (self.__umlsDict[umls], MAX_JACCARD_INDEX) if umls in self.__umlsDict else (None, None)

    def GetByGard(self, gard):
        return (self.__gardDict[gard], MAX_JACCARD_INDEX) if gard in self.__gardDict else (None, None)

    def GetByMesh(self, mesh):
        return (self.__meshDict[mesh], MAX_JACCARD_INDEX) if mesh in self.__meshDict else (None, None)

    def GetByMedDra(self, medDra):
        return (self.__medDraDict[medDra], MAX_JACCARD_INDEX) if medDra in self.__medDraDict else (None, None)

    def GetByIcd10(self, icd10):
        return (self.__icd10Dict[icd10], MAX_JACCARD_INDEX) if icd10 in self.__icd10Dict else (None, None)

    def GetByXref(self, xref, value):
        if xref == Xref.OMIM:
            return self.GetByOmim(value)
        elif xref == Xref.UMLS:
            return self.GetByUmls(value)
        elif xref == Xref.GARD:
            return self.GetByGard(value)
        elif xref == Xref.MeSH:
            return self.GetByMesh(value)
        elif xref == Xref.MedDRA:
            return self.GetByMedDra(value)
        elif xref == Xref.ICD10:
            return self.GetByIcd10(value)

    def GetByDiseaseNameWithoutSearchEngine(self, diseaseName):
        if diseaseName is None:
            return None, None

        preprocessedDiseaseName = frozenset(PreprocessingDiseaseName(diseaseName))
        if preprocessedDiseaseName in self.__diseaseNameFrozenSetDict:
            return self.__diseaseNameFrozenSetDict[preprocessedDiseaseName], MAX_JACCARD_INDEX

        return None, None

    def GetByDiseaseName(self, diseaseName):
        if diseaseName is None:
            return None, None

        preprocessedDiseaseName = PreprocessingDiseaseName(diseaseName)
        preprocessedDiseaseNameFrozenSet = frozenset(preprocessedDiseaseName)
        if preprocessedDiseaseNameFrozenSet in self.__diseaseNameFrozenSetDict:
            return self.__diseaseNameFrozenSetDict[preprocessedDiseaseNameFrozenSet], MAX_JACCARD_INDEX
        else:
            return self.__SearchWithSearchEngine(preprocessedDiseaseName)

    # TODO: add check if we have more than one hit then we can compare results with Jaccard index or some other measure
    def __SearchWithSearchEngine(self, preprocessedDiseaseNameTokens):
        preprocessedDiseaseName = ' '.join(preprocessedDiseaseNameTokens)
        searchResult = self.__searchEngineClient. \
            SearchByQuery(COLLECTION_NAME_DOID, preprocessedDiseaseName, QUERY_BY_DOID)
        if len(searchResult["hits"]) > 0:
            foundDiseaseName = searchResult["hits"][0]["document"]["diseaseName"]
            jaccSimilarity = JaccardSimilarity(foundDiseaseName, preprocessedDiseaseName)
            doid = searchResult["hits"][0]["document"]["doid"]
            # self.__diseaseNameFrozenSetDict[frozenset(preprocessedDiseaseNameTokens)] = doid
            return doid, jaccSimilarity
        elif " due " in preprocessedDiseaseName:
            return self.GetByDiseaseName(preprocessedDiseaseName.split(" due ")[0])
        elif " with without " in preprocessedDiseaseName:
            return self.GetByDiseaseName(preprocessedDiseaseName.split(" with without ")[0])
        elif " with " in preprocessedDiseaseName:
            return self.GetByDiseaseName(preprocessedDiseaseName.split(" with ")[0])
        elif " without " in preprocessedDiseaseName:
            return self.GetByDiseaseName(preprocessedDiseaseName.split(" without ")[0])

        return None, None


# DiseaseName is part of: DisGeNet, Cosmic, HumsaVar, Orphanet, ClinVar, Diseases, OBO
# DiseaseName can be found using DOID (OBO and Diseases), Omim and Orpha
class DiseaseName:
    def __init__(self, doidDict, orphaDict, omimDict):
        self.__doidDict = doidDict
        self.__orphaDict = orphaDict
        self.__omimDict = omimDict

    def GetByDoid(self, doid):
        return self.__doidDict[doid] if doid in self.__doidDict else None

    def GetByOrpha(self, orpha):
        return self.__orphaDict[orpha] if orpha in self.__orphaDict else None

    def GetByOmim(self, omim):
        return self.__omimDict[omim] if omim in self.__omimDict else []


# Xrefs can be found by Orpha and can be returned only exact xref values, not exact xref values or all xref values
class Xrefs:
    def __init__(self, orphaExactDict, orphaNotExactDict, orphaDict):
        self.__orphaExactDict = orphaExactDict
        self.__orphaNotExactDict = orphaNotExactDict
        self.__orphaDict = orphaDict

    def GetByOrpha(self, orpha):
        return self.__orphaDict[orpha] if orpha in self.__orphaDict else {}

    def GetByOrphaExact(self, orpha):
        return self.__orphaExactDict[orpha] if orpha in self.__orphaExactDict else {}

    def GetByOrphaNotExact(self, orpha):
        return self.__orphaNotExactDict[orpha] if orpha in self.__orphaNotExactDict else {}

