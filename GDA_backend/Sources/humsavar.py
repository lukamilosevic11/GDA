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

from GDA_backend.Classes.annotation_row import HumsaVarRow
from GDA_backend.Common.constants import HUMSAVAR_PATH
from GDA_backend.Common.init import OrderedSet
from GDA_backend.Common.util import CheckEmpty


class HumsaVar:
    @staticmethod
    def Read(filePath=HUMSAVAR_PATH):
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
