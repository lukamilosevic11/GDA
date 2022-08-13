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

from GDA_backend.Classes.annotation_models import DisGeNetRow, CosmicRow, HumsaVarRow, OrphanetRow, ClinVarRow, HPORow, \
    DiseasesRow
from GDA_backend.Common.constants import DISGENET_PATH, COSMIC_PATH, HUMSAVAR_PATH, ORPHANET_PATH, CLINVAR_PATH, \
    HPO_PATH, DISEASES_PATH
from GDA_backend.Common.init import pd, et, OrderedSet
from GDA_backend.Common.util import CheckNan, CheckEmpty


class SourceInput:
    @staticmethod
    def ReadDisGeNet(filePath=DISGENET_PATH):
        disGeNetData = pd.read_csv(filePath, sep='\t', dtype=str)
        disGeNetData = disGeNetData[["geneId", "geneSymbol", "diseaseId", "diseaseName"]]
        disGeNetData = disGeNetData.to_numpy()

        disGeNetSet = OrderedSet()
        for row in disGeNetData:
            symbol = CheckNan(row[1])
            entrezID = CheckNan(row[0])
            umls = CheckNan(row[2])
            diseaseName = CheckNan(row[3])
            disGeNetSet.add(DisGeNetRow(symbol, entrezID, diseaseName, umls))

        return disGeNetSet

    @staticmethod
    def ReadCosmic(filePath=COSMIC_PATH):
        cosmicData = pd.read_csv(filePath, sep=',', dtype=str)
        cosmicData = cosmicData[["Gene Symbol", "Entrez GeneId", "Tumour Types(Somatic)", "Tumour Types(Germline)"]]
        cosmicData = cosmicData.to_numpy()

        cosmicSet = OrderedSet()
        for row in cosmicData:
            symbol = CheckNan(row[0])
            entrezID = CheckNan(row[1])
            diseaseNameSomatic = CheckNan(row[2])
            diseaseNameGermline = CheckNan(row[3])
            if diseaseNameSomatic is not None:
                cosmicSet.add(CosmicRow(symbol, entrezID, diseaseNameSomatic))
            if diseaseNameGermline is not None:
                cosmicSet.add(CosmicRow(symbol, entrezID, diseaseNameGermline))

        return cosmicSet

    @staticmethod
    def ReadHumsaVar(filePath=HUMSAVAR_PATH):
        humsavarSet = OrderedSet()
        with open(filePath, 'r') as humsavarFile:
            humsavarLines = humsavarFile.readlines()
            takeLine = False
            for line in humsavarLines:
                if "_________" in line.strip():
                    takeLine = True
                    continue
                elif line.strip() == "":
                    takeLine = False

                if takeLine:
                    lineSplitted = ' '.join(line.strip().split()).split(" ", 6)
                    if len(lineSplitted) >= 7 and lineSplitted[4].strip() != "US" and lineSplitted[6].strip() != "-":
                        symbol = CheckEmpty(lineSplitted[0])
                        uniprotID = CheckEmpty(lineSplitted[1])
                        diseaseNameAndOmim = lineSplitted[6].strip().rsplit(" ", 2)
                        diseaseName = diseaseNameAndOmim[0].strip()
                        omim = diseaseNameAndOmim[2].strip().split(":")[1][:-1].strip()
                        humsavarSet.add(HumsaVarRow(symbol, uniprotID, diseaseName, omim))

        return humsavarSet

    @staticmethod
    def ReadOrphanet(filePath=ORPHANET_PATH):
        orphanetSet = OrderedSet()
        tree = et.parse(filePath)
        root = tree.getroot()
        disorderList = root.find("DisorderList")
        for disorder in disorderList:
            disorderType = disorder.find("DisorderType").find("Name").text.strip()
            if disorderType != "Disease":
                continue

            orpha = disorder.find("OrphaCode").text.strip()
            diseaseName = disorder.find("Name").text.strip()
            disorderGeneAssociationList = disorder.find("DisorderGeneAssociationList")
            for disorderGeneAssociation in disorderGeneAssociationList:
                gene = disorderGeneAssociation.find("Gene")
                symbol = gene.find("Symbol").text.strip()

                externalReferenceList = gene.find("ExternalReferenceList")
                ensemblID = None
                uniprotID = None
                for externalReference in externalReferenceList:
                    source = externalReference.find("Source").text.strip()
                    if source == "Ensembl":
                        ensemblID = externalReference.find("Reference").text.strip()
                    elif source == "SwissProt":
                        uniprotID = externalReference.find("Reference").text.strip()

                orphanetSet.add(OrphanetRow(symbol, uniprotID, ensemblID, diseaseName, orpha))

        return orphanetSet

    @staticmethod
    def ReadClinVar(filePath=CLINVAR_PATH):
        clinVarData = pd.read_csv(filePath, sep='\t', dtype=str)
        clinVarData = clinVarData[["#GeneID", "AssociatedGenes", "RelatedGenes", "ConceptID", "DiseaseName",
                                   "DiseaseMIM"]]
        clinVarData = clinVarData.to_numpy()

        clinVarSet = OrderedSet()
        for row in clinVarData:
            associatedGeneSymbol = CheckNan(row[1])
            relatedGeneSymbol = CheckNan(row[2])
            entrezID = CheckNan(row[0])
            diseaseName = CheckNan(row[4])
            umls = CheckNan(row[3])
            omim = CheckNan(row[5])
            if associatedGeneSymbol is not None:
                clinVarSet.add(ClinVarRow(associatedGeneSymbol, entrezID, diseaseName, umls, omim))

            if relatedGeneSymbol is not None:
                clinVarSet.add(ClinVarRow(relatedGeneSymbol, entrezID, diseaseName, umls, omim))

        return clinVarSet

    @staticmethod
    def ReadHPO(filePath=HPO_PATH):
        hpoSet = OrderedSet()
        with open(filePath, 'r') as hpoFile:
            hpoLines = hpoFile.readlines()
            for line in hpoLines[1:]:
                splittedLine = line.strip().split('\t')
                symbol = CheckEmpty(splittedLine[1])
                entrezID = CheckEmpty(splittedLine[0])
                omim = None
                orpha = None
                omimOrpha = CheckEmpty(splittedLine[8])
                if omimOrpha is not None:
                    omimOrphaSplitted = omimOrpha.split(":")
                    if omimOrphaSplitted[0] == "OMIM":
                        omim = omimOrphaSplitted[1]
                    elif omimOrphaSplitted[0] == "ORPHA":
                        orpha = omimOrphaSplitted[1]

                hpoSet.add(HPORow(symbol, entrezID, omim, orpha))

        return hpoSet

    @staticmethod
    def ReadDiseases(obsoleteDOIDs, filePath=DISEASES_PATH):
        diseasesData = pd.read_csv(filePath, sep='\t', header=None, usecols=[0, 1, 2, 3], dtype=str)
        diseasesData = diseasesData.to_numpy()

        diseasesSet = OrderedSet()
        for row in diseasesData:
            doid = CheckNan(row[2])
            if doid in obsoleteDOIDs:
                continue

            ensemblProteinID = CheckNan(row[0])
            if ensemblProteinID is not None and not ensemblProteinID.startswith("ENSP"):
                ensemblProteinID = None

            symbol = CheckNan(row[1])
            if symbol is not None and symbol.startswith("ENSP"):
                symbol = None

            diseaseName = CheckNan(row[3])
            if "DOID:" in diseaseName:
                diseaseName = None

            diseasesSet.add(DiseasesRow(symbol, doid, diseaseName, ensemblProteinID))

        return diseasesSet
