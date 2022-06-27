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

from Classes.event import Subject, Observer
from Classes.parsing_context_thread import ParsingContextThread
from Common.init import time, Lock
from Other.measurements import DoidAccuracy


def main():
    progressSubject = Subject(Lock())
    observer = Observer()
    progressSubject.attach(observer)
    startTime = time.time()
    parsingContext = ParsingContextThread(progressSubject)
    parsingContextEndTime = time.time()
    print("Time processing parsing context: {}".format(parsingContextEndTime - startTime))
    tmpFilePath = "./Storage/annotation_file.txt"
    tmpDoidAccuracyPath = "./Storage/doid_accuracy.txt"
    startTimeAnnotationFile = time.time()
    print("Time processing Final annotation file: {}".format(startTimeAnnotationFile - parsingContextEndTime))
    parsingContext.CreateAnnotationFile(tmpFilePath)
    AnnotationFileWritingEndTime = time.time()
    print("Time processing writing final annotatiton file: {}"
          .format(AnnotationFileWritingEndTime - startTimeAnnotationFile))
    print("Total time: {}".format(AnnotationFileWritingEndTime - startTime))
    DoidAccuracy(tmpFilePath, tmpDoidAccuracyPath)


if __name__ == '__main__':
    main()
