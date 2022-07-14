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

from GDA_backend.Common.constants import COLLECTION_NAME_DOID, QUERY_BY_DOID, DOID_SOURCE_XREF_OMIM, \
    DOID_SOURCE_XREF_UMLS, DOID_SOURCE_XREF_MESH, DOID_SOURCE_XREF_GARD, DOID_SOURCE_XREF_MEDDRA, \
    DOID_SOURCE_XREF_ICD10, DOID_SOURCE_SEARCH_ENGINE, DOID_SOURCE_FROZEN_SET
from GDA_backend.Common.init import Xref
from GDA_backend.Common.util import PreprocessingDiseaseName, JaccardSimilarity


# Symbol is part of all sources
# Symbol can be found using entrezID, ensemblID and uniprotID
class Symbol:
    def __init__(self, entrezIDDict, ensemblIDDict, uniprotIDDict):
        self.__entrezIDDict = entrezIDDict
        self.__ensemblIDDict = ensemblIDDict
        self.__uniprotIDDict = uniprotIDDict

    def GetByEntrezID(self, entrezID):
        return self.__entrezIDDict[entrezID] if entrezID in self.__entrezIDDict else None

    def GetByEnsemblID(self, ensemblID):
        return self.__ensemblIDDict[ensemblID] if ensemblID in self.__ensemblIDDict else None

    def GetByUniprotID(self, uniprotID):
        return self.__uniprotIDDict[uniprotID] if uniprotID in self.__uniprotIDDict else None


# EntrezID is part of: DisGeNet, Cosmic, ClinVar, HPO, Uniprot, Hugo, Ensembl
# EntrezID can be found using symbol, ensemblID, uniprotID, ensemblProteinID
class EntrezID:
    def __init__(self, symbolDict, ensemblIDDict, uniprotIDDict, ensemblProteinIDDict):
        self.__symbolDict = symbolDict
        self.__ensemblIDDict = ensemblIDDict
        self.__uniprotIDDict = uniprotIDDict
        self.__ensemblProteinIDDict = ensemblProteinIDDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEnsemblID(self, ensemblID):
        return self.__ensemblIDDict[ensemblID] if ensemblID in self.__ensemblIDDict else None

    def GetByUniprotID(self, uniprotID):
        return self.__uniprotIDDict[uniprotID] if uniprotID in self.__uniprotIDDict else None

    def GetByEnsemblProteinID(self, ensemblProteinID):
        return self.__ensemblProteinIDDict[
            ensemblProteinID] if ensemblProteinID in self.__ensemblProteinIDDict else None


# UniprotID is part of: Uniprot, Hugo, Ensembl
# UniprotID can be found using symbol, entrezID, ensemblID, ensemblProteinID
class UniprotID:
    def __init__(self, symbolDict, entrezIDDict, ensemblIDDict, ensemblProteinIDDict):
        self.__symbolDict = symbolDict
        self.__entrezIDDict = entrezIDDict
        self.__ensemblIDDict = ensemblIDDict
        self.__ensemblProteinIDDict = ensemblProteinIDDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEntrezID(self, entrezID):
        return self.__entrezIDDict[entrezID] if entrezID in self.__entrezIDDict else None

    def GetByEnsemblID(self, ensemblID):
        return self.__ensemblIDDict[ensemblID] if ensemblID in self.__ensemblIDDict else None

    def GetByEnsemblProteinID(self, ensemblProteinID):
        return self.__ensemblProteinIDDict[
            ensemblProteinID] if ensemblProteinID in self.__ensemblProteinIDDict else None


# EnsemblID is part of: Orphanet ,Uniprot, Hugo, Ensembl
# EnsemblID can be found using symbol, entrezID, uniprotID, ensemblProteinID
class EnsemblID:
    def __init__(self, symbolDict, entrezIDDict, uniprotIDDict, ensemblProteinIDDict):
        self.__symbolDict = symbolDict
        self.__entrezIDDict = entrezIDDict
        self.__uniprotIDDict = uniprotIDDict
        self.__ensemblProteinIDDict = ensemblProteinIDDict

    def GetBySymbol(self, symbol):
        return self.__symbolDict[symbol] if symbol in self.__symbolDict else None

    def GetByEntrezID(self, entrezID):
        return self.__entrezIDDict[entrezID] if entrezID in self.__entrezIDDict else None

    def GetByUniprotID(self, uniprotID):
        return self.__uniprotIDDict[uniprotID] if uniprotID in self.__uniprotIDDict else None

    def GetByEnsemblProteinID(self, ensemblProteinID):
        return self.__ensemblProteinIDDict[
            ensemblProteinID] if ensemblProteinID in self.__ensemblProteinIDDict else None


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
        return (self.__omimDict[omim], DOID_SOURCE_XREF_OMIM) if omim in self.__omimDict else (None, None)

    def GetByUmls(self, umls):
        return (self.__umlsDict[umls], DOID_SOURCE_XREF_UMLS) if umls in self.__umlsDict else (None, None)

    def GetByGard(self, gard):
        return (self.__gardDict[gard], DOID_SOURCE_XREF_GARD) if gard in self.__gardDict else (None, None)

    def GetByMesh(self, mesh):
        return (self.__meshDict[mesh], DOID_SOURCE_XREF_MESH) if mesh in self.__meshDict else (None, None)

    def GetByMedDra(self, medDra):
        return (self.__medDraDict[medDra], DOID_SOURCE_XREF_MEDDRA) if medDra in self.__medDraDict else (None, None)

    def GetByIcd10(self, icd10):
        return (self.__icd10Dict[icd10], DOID_SOURCE_XREF_ICD10) if icd10 in self.__icd10Dict else (None, None)

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
            return self.__diseaseNameFrozenSetDict[preprocessedDiseaseName], DOID_SOURCE_FROZEN_SET

        return None, None

    def GetByDiseaseName(self, diseaseName):
        if diseaseName is None:
            return None, None

        preprocessedDiseaseName = PreprocessingDiseaseName(diseaseName)
        preprocessedDiseaseNameFrozenSet = frozenset(preprocessedDiseaseName)
        if preprocessedDiseaseNameFrozenSet in self.__diseaseNameFrozenSetDict:
            return self.__diseaseNameFrozenSetDict[preprocessedDiseaseNameFrozenSet], DOID_SOURCE_FROZEN_SET
        else:
            return self.__SearchWithSearchEngine(preprocessedDiseaseName)

    def __SearchWithSearchEngine(self, preprocessedDiseaseNameTokens):
        preprocessedDiseaseName = ' '.join(preprocessedDiseaseNameTokens)
        searchResult = self.__searchEngineClient. \
            SearchByQuery(COLLECTION_NAME_DOID, preprocessedDiseaseName, QUERY_BY_DOID)
        if len(searchResult["hits"]) > 0:
            foundDiseaseName = searchResult["hits"][0]["document"]["diseaseName"]
            jaccSimilarity = JaccardSimilarity(foundDiseaseName, preprocessedDiseaseName)
            doid = searchResult["hits"][0]["document"]["doid"]
            doidSource = DOID_SOURCE_SEARCH_ENGINE + ", " + str(int(round(jaccSimilarity * 100, 0))) + '%'

            return doid, doidSource
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
    def __init__(self, doidDict, orphaDict, omimDiseaseNameDict, omimDoidAndDiseaseNameDict, doidParentDict):
        self.__doidDict = doidDict
        self.__orphaDict = orphaDict
        self.__omimDiseaseNameDict = omimDiseaseNameDict
        self.__omimDoidAndDiseaseNameDict = omimDoidAndDiseaseNameDict
        self.__doidParentDict = doidParentDict

    def GetByDoid(self, doid):
        return self.__doidDict[doid] if doid in self.__doidDict else None

    def GetByOrpha(self, orpha):
        return self.__orphaDict[orpha] if orpha in self.__orphaDict else None

    def GetByOmim(self, omim):
        return self.__omimDiseaseNameDict[omim] if omim in self.__omimDiseaseNameDict else []

    def GetByOmimDoidAndDiseaseName(self, omim):
        return self.__omimDoidAndDiseaseNameDict[omim] if omim in self.__omimDoidAndDiseaseNameDict else []

    def GetParentDoidAndDiseaseNamesByDoid(self, doid):
        return self.__doidParentDict[doid] if doid in self.__doidParentDict else []


# Xrefs can be found by Orpha and can be returned only exact xref values, not exact xref values or all xref values
class Xrefs:
    def __init__(self, orphaExactDict, orphaBtntDict, orphaNtbtDict, orphaOtherDict):
        self.__orphaExactDict = orphaExactDict
        self.__orphaBtntDict = orphaBtntDict
        self.__orphaNtbtDict = orphaNtbtDict
        self.__orphaOtherDict = orphaOtherDict

    def GetByOrphaExact(self, orpha):
        return self.__orphaExactDict[orpha] if orpha in self.__orphaExactDict else {}

    def GetByOrphaBtnt(self, orpha):
        return self.__orphaBtntDict[orpha] if orpha in self.__orphaBtntDict else {}

    def GetByOrphaNtbt(self, orpha):
        return self.__orphaNtbtDict[orpha] if orpha in self.__orphaNtbtDict else {}

    def GetByOrphaOther(self, orpha):
        return self.__orphaOtherDict[orpha] if orpha in self.__orphaOtherDict else {}
