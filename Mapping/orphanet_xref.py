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
from Common.init import et, Xref, OrderedDict, OrderedSet


class OrphanetXref:
    @staticmethod
    def Read(filePath=ORPHANET_XREF_PATH):
        orphanetXrefSet = OrderedSet()
        tree = et.parse(filePath)
        root = tree.getroot()
        disorderList = root.find("DisorderList")
        for disorder in disorderList:
            disorderType = disorder.find("DisorderType").find("Name").text.strip()
            if disorderType != "Disease":
                continue

            orpha = disorder.find("OrphaCode").text.strip()
            diseaseName = disorder.find("Name").text.strip()
            eDict = {}
            btntDict = {}
            ntbtDict = {}
            otherDict = {}

            def addValueToMappingRelationDict(xref, valueP, mappingRelationP):
                if mappingRelationP == 'E':
                    if xref not in eDict:
                        eDict[xref] = {valueP}
                    else:
                        eDict[xref].add(valueP)
                elif mappingRelationP == "BTNT":
                    if xref not in btntDict:
                        btntDict[xref] = {valueP}
                    else:
                        btntDict[xref].add(valueP)
                elif mappingRelationP == "NTBT":
                    if xref not in ntbtDict:
                        ntbtDict[xref] = {valueP}
                    else:
                        ntbtDict[xref].add(valueP)
                else:
                    if xref not in otherDict:
                        otherDict[xref] = {valueP}
                    else:
                        otherDict[xref].add(valueP)

            externalReferenceList = disorder.find("ExternalReferenceList")
            for externalReference in externalReferenceList:
                source = externalReference.find("Source").text.strip()
                value = externalReference.find("Reference").text.strip()
                mappingRelation = externalReference.find("DisorderMappingRelation").find("Name").text.strip().split()[0]

                if source == "OMIM":
                    addValueToMappingRelationDict(Xref.OMIM, value, mappingRelation)
                elif source == "UMLS":
                    addValueToMappingRelationDict(Xref.UMLS, value, mappingRelation)
                elif source == "MeSH":
                    addValueToMappingRelationDict(Xref.MeSH, value, mappingRelation)
                elif source == "GARD":
                    addValueToMappingRelationDict(Xref.GARD, value, mappingRelation)
                elif source == "MedDRA":
                    addValueToMappingRelationDict(Xref.MedDRA, value, mappingRelation)
                elif source == "ICD-10":
                    addValueToMappingRelationDict(Xref.ICD10, value, mappingRelation)

            eDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), eDict.items())))
            btntDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), btntDict.items())))
            ntbtDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), ntbtDict.items())))
            otherDict = OrderedDict(sorted(map(lambda x: (x[0], sorted(x[1])), otherDict.items())))

            orphanetXrefSet.add(OrphanetXrefRow(orpha, eDict, btntDict, ntbtDict, otherDict, diseaseName))

        return orphanetXrefSet
