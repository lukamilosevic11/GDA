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

from Classes.annotation_row import OrphanetXrefRow
from Common.constants import ORPHANET_XREF_PATH
from Common.init import et


class OrphanetXref:
    @staticmethod
    def Read(filePath=ORPHANET_XREF_PATH):
        orphanetXrefSet = set()
        tree = et.parse(filePath)
        root = tree.getroot()
        disorderList = root.find("DisorderList")
        for disorder in disorderList:
            disorderType = disorder.find("DisorderType").find("Name").text.strip()
            if disorderType != "Disease":
                continue

            orpha = disorder.find("OrphaCode").text.strip()
            diseaseName = disorder.find("Name").text.strip()
            omim = None
            umls = None
            mesh = None
            gard = None
            medDra = None
            icd10 = None
            externalReferenceList = disorder.find("ExternalReferenceList")
            for externalReference in externalReferenceList:
                source = externalReference.find("Source").text.strip()
                value = externalReference.find("Reference").text.strip()
                mappingRelation = externalReference.find("DisorderMappingRelation").find("Name").text.strip().split()[0]
                exactFlag = True if mappingRelation == 'E' else False
                if source == "OMIM":
                    if omim is None:
                        omim = (value, exactFlag)
                    elif not omim[1] and exactFlag:
                        omim = (value, exactFlag)
                elif source == "UMLS":
                    if umls is None:
                        umls = (value, exactFlag)
                    elif not umls[1] and exactFlag:
                        umls = (value, exactFlag)
                elif source == "MeSH":
                    if mesh is None:
                        mesh = (value, exactFlag)
                    elif not mesh[1] and exactFlag:
                        mesh = (value, exactFlag)
                elif source == "GARD":
                    if gard is None:
                        gard = (value, exactFlag)
                    elif not gard[1] and exactFlag:
                        gard = (value, exactFlag)
                elif source == "MedDRA":
                    if medDra is None:
                        medDra = (value, exactFlag)
                    elif not medDra[1] and exactFlag:
                        medDra = (value, exactFlag)
                elif source == "ICD-10":
                    if icd10 is None:
                        icd10 = (value, exactFlag)
                    elif not icd10[1] and exactFlag:
                        icd10 = (value, exactFlag)

            orphanetXrefSet.add(OrphanetXrefRow(orpha, omim, umls, mesh, gard, medDra, icd10, diseaseName))

        return orphanetXrefSet
