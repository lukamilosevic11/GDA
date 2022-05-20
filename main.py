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

from Classes.parsing_context import ParsingContext
from Common.init import time


def main():
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

    startTime = time.time()
    parsingContext = ParsingContext(True)
    parsingContextEndTime = time.time()
    print("Time processing parsing context: {}".format(parsingContextEndTime - startTime))
    tmpFilePath = "./Results/annotationFile.txt"
    startTimeAnnotationFile = time.time()
    print("Time processing Final annotation file: {}".format(startTimeAnnotationFile - parsingContextEndTime))
    parsingContext.CreateAnnotationFile(tmpFilePath)
    AnnotationFileWritingEndTime = time.time()
    print("Time processing writing final annotatiton file: {}"
          .format(AnnotationFileWritingEndTime - startTimeAnnotationFile))
    print("Total time: {}".format(AnnotationFileWritingEndTime - startTime))

    # util.writeJsonSetToFile("./Results/tmp.jsonl", oboSet, [Attribute.DOID, Attribute.DISEASE_NAME], Source.OBO)
    # util.writeSetToFile(tmpFilePath, parsingContext.dbContext.uniprot)
    # print(len(parsingContext.annotationContext.entrezID.symbolDict))
    # print(' '.join(util.preprocessingDiseaseName("Schizophrenia-like symptoms (uncommon)")))


if __name__ == '__main__':
    main()
