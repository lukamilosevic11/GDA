#  GDA Copyright (c) 2021.
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

from Classes.parsing_context_thread import ParsingContextThread
from Common.init import time
from Sources.hpo import HPO
from Common.util import WriteStructureToFile, PrintStructure, PreprocessingDiseaseName, JaccardSimilarity
from Mapping.obo import OBO
from Sources.orphanet import Orphanet
from Sources.humsavar import HumsaVar
from Mapping.orphanet_xref import OrphanetXref
from Other.measurements import DoidAccuracy


def main():
    # a = JaccardSimilarity(PreprocessingDiseaseName("syndromic X-linked intellectual disability Raymond type", True), PreprocessingDiseaseName("Severe intellectual disability-progressive postnatal microcephaly-midline stereotypic hand movements syndrome", True))
    # b = JaccardSimilarity(PreprocessingDiseaseName("non-syndromic X-linked intellectual disability 1", True), PreprocessingDiseaseName("Severe intellectual disability-progressive postnatal microcephaly-midline stereotypic hand movements syndrome", True))
    # if a > b:
    #     print("da", a, b)
    # else:
    #     print("ne", a, b)
    # DoidAccuracy("./Results/annotationFile1.txt")
    # oboSet = OBO.Read()
    # for row in oboSet:
    #     parentDoids = row.GetParentDiseaseNameAndDoids()
    #     print(row.doid, parentDoids)
    #     altIds = row.GetAlternateIds()
    #     if altIds:
    #         # for altid in altIds:
    #         #     splitted = altid.split(':')
    #         #     if len(splitted) == 1:
    #         #         print(splitted)
    #         # print()
    #         print(altIds)
    # orphanetSet = Orphanet.Read()
    # hpoSet = HPO.Read()
    # humsavarSet = HumsaVar.Read()
    # orphanetXrefSet = OrphanetXref.Read()
    # PrintStructure(orphanetXrefSet)
    # for row in orphanetXrefSet:
    #     exact = row.GetExactXrefs()
    #     if exact:
    #         print(exact)
    # for row in oboSet:
    # for xref in row.GetAlternateIds():
    # print(xref.split(':'))
    # print()
    # print(row.GetAlternateIds())
    # print()
    # PrintStructure(oboSet)
    # WriteStructureToFile('Results/oboSet.txt', oboSet)

    # startTime = time.time()
    # parsingContext = ParsingContext(True)
    # parsingContextTime = time.time()
    # print("Time processing parsing context: {}".format(parsingContextTime - startTime))
    # tmpFilePath = "./Results/tmp.txt"
    # disGeNetDoidSet = set()
    # for row in parsingContext.dbContext.disGeNet:
    #     doid = str(parsingContext.annotationContext.doid.GetByDiseaseName(row.diseaseName))
    #     disGeNetDoidSet.add(row.diseaseName + " " +
    #                         doid + " " + str(parsingContext.annotationContext.diseaseName.GetByDoid(doid)))
    # disGeNetDoidTime = time.time()
    # print("Time processing disGeNet doid: {}".format(disGeNetDoidTime - parsingContextTime))
    # util.writeSetToFile(tmpFilePath, disGeNetDoidSet)
    # disGeNetDoidWritingSetTime = time.time()
    # print("Time processing writing disGeNetSet doid: {}".format(disGeNetDoidWritingSetTime - disGeNetDoidTime))
    # print("Total time: {}".format(disGeNetDoidWritingSetTime - startTime))

    # *********************************************************************************************************
    startTime = time.time()
    parsingContext = ParsingContextThread(True)
    parsingContextEndTime = time.time()
    print("Time processing parsing context: {}".format(parsingContextEndTime - startTime))
    tmpFilePath = "./Results/annotationFile3.txt"
    startTimeAnnotationFile = time.time()
    print("Time processing Final annotation file: {}".format(startTimeAnnotationFile - parsingContextEndTime))
    parsingContext.CreateAnnotationFile(tmpFilePath)
    AnnotationFileWritingEndTime = time.time()
    print("Time processing writing final annotatiton file: {}"
          .format(AnnotationFileWritingEndTime - startTimeAnnotationFile))
    print("Total time: {}".format(AnnotationFileWritingEndTime - startTime))
    DoidAccuracy(tmpFilePath)
    # *********************************************************************************************************

    # startTime = time.time()
    # parsingContext = ParsingContextThread(True)
    # parsingContextEndTime = time.time()
    # print("Time processing parsing context: {}".format(parsingContextEndTime - startTime))
    # tmpFilePath = "./Results/annotationFile.txt"
    # startTimeAnnotationFile = time.time()
    # print("Time processing Final annotation file: {}".format(startTimeAnnotationFile - parsingContextEndTime))
    # parsingContext.CreateAnnotationFile(tmpFilePath)
    # AnnotationFileWritingEndTime = time.time()
    # print("Time processing writing final annotatiton file: {}"
    #       .format(AnnotationFileWritingEndTime - startTimeAnnotationFile))
    # datatablesFilePath = "./DataTables/index.html"
    # datatables = DataTables(tmpFilePath)
    # datatables.CreateDataTableHTML(datatablesFilePath)
    # datatablesTime = time.time()
    # print("Time processing datatables: {}".format(datatablesTime-AnnotationFileWritingEndTime))
    # print("Total time: {}".format(datatablesTime - startTime))

    # hpoSet = HPO.Read()

    # util.writeJsonSetToFile("./Results/tmp.jsonl", oboSet, [Attribute.DOID, Attribute.DISEASE_NAME], Source.OBO)
    # WriteStructureToFile("./Results/hpoTest.txt", hpoSet)
    # print(len(parsingContext.annotationContext.entrezID.symbolDict))
    # print(' '.join(util.preprocessingDiseaseName("Schizophrenia-like symptoms (uncommon)")))


if __name__ == '__main__':
    main()
