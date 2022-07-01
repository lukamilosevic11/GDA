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

from GDA_backend.Classes.parsing_context_thread import ParsingContextThread
from GDA_backend.Common.constants import ANNOTATION_PATH, DOID_ACCURACY_PATH
from GDA_backend.Common.init import time
from GDA_backend.Common.util import PrintElapsedTime
from GDA_backend.Other.measurements import DoidAccuracy


class Parsing:
    @staticmethod
    def parse(progress, initializeSearchEngine=False):
        startTime = time.time()
        parsingContext = ParsingContextThread(progress, initializeSearchEngine)
        parsingContext.CreateAnnotationFile(ANNOTATION_PATH)
        DoidAccuracy(ANNOTATION_PATH, DOID_ACCURACY_PATH)
        PrintElapsedTime(startTime, time.time(), "Total elapsed time")
