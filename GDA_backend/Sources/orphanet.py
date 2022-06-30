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

from GDA_backend.Classes.annotation_row import OrphanetRow
from GDA_backend.Common.constants import ORPHANET_PATH
from GDA_backend.Common.init import et, OrderedSet


class Orphanet:
    @staticmethod
    def Read(filePath=ORPHANET_PATH):
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
                for externalReference in externalReferenceList:
                    source = externalReference.find("Source").text.strip()
                    if source != "Ensembl":
                        continue

                    ensemblID = externalReference.find("Reference").text.strip()

                    orphanetSet.add(OrphanetRow(symbol, ensemblID, diseaseName, orpha))

        return orphanetSet
