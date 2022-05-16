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

from Classes import annotation_row as ar
from Common import init, util, constants


class Diseases:
    @staticmethod
    def Read(filePath=constants.DISEASES_PATH):
        diseasesData = init.PD.read_csv(filePath, sep='\t', header=None, usecols=[1, 2, 3], dtype=str)
        diseasesData = diseasesData.to_numpy()

        diseasesSet = set()
        for row in diseasesData:
            symbol = util.checkNan(row[0])
            doid = util.checkNan(row[1])
            diseaseName = util.checkNan(row[2])
            diseasesSet.add(ar.DiseasesRow(symbol, doid, diseaseName))

        return diseasesSet
