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

from Classes.annotation_row import HPORow
from Common.constants import HPO_PATH
from Common.util import CheckEmpty


class HPO:
    @staticmethod
    def Read(filePath=HPO_PATH):
        hpoSet = set()
        with open(filePath, 'r') as hpoFile:
            hpoLines = hpoFile.readlines()
            for line in hpoLines[1:]:
                splittedLine = line.strip().split('\t')
                symbol = CheckEmpty(splittedLine[1])
                entrezID = CheckEmpty(splittedLine[0])
                diseaseName = CheckEmpty(splittedLine[3])
                hpoSet.add(HPORow(symbol, entrezID, diseaseName))

        return hpoSet
