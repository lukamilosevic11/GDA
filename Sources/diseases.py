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

from Classes.annotation_row import DiseasesRow
from Common.constants import DISEASES_PATH
from Common.init import pd, OrderedSet
from Common.util import CheckNan, CheckEmpty


class Diseases:
    @staticmethod
    def Read(filePath=DISEASES_PATH):
        diseasesData = pd.read_csv(filePath, sep='\t', header=None, usecols=[1, 2, 3], dtype=str)
        diseasesData = diseasesData.to_numpy()

        diseasesSet = OrderedSet()
        for row in diseasesData:
            symbol = CheckEmpty(CheckNan(row[0]))
            doid = CheckEmpty(CheckNan(row[1]))
            diseaseName = CheckEmpty(CheckNan(row[2]))
            diseasesSet.add(DiseasesRow(symbol, doid, diseaseName))

        return diseasesSet
