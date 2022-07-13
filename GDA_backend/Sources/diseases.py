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

from GDA_backend.Classes.annotation_row import DiseasesRow
from GDA_backend.Common.constants import DISEASES_PATH
from GDA_backend.Common.init import pd, OrderedSet
from GDA_backend.Common.util import CheckNan, CheckEmpty


class Diseases:
    @staticmethod
    def Read(obsoleteDOIDs, filePath=DISEASES_PATH):
        diseasesData = pd.read_csv(filePath, sep='\t', header=None, usecols=[1, 2, 3], dtype=str)
        diseasesData = diseasesData.to_numpy()

        diseasesSet = OrderedSet()
        for row in diseasesData:
            doid = CheckNan(row[1])
            if doid in obsoleteDOIDs:
                continue

            symbol = CheckNan(row[0])
            diseaseName = CheckNan(row[2])
            if "DOID:" in diseaseName:
                diseaseName = None

            diseasesSet.add(DiseasesRow(symbol, doid, diseaseName))

        return diseasesSet
