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

from Classes import annotationrow as ar
from common import init, util


class Cosmic:
    @staticmethod
    def Read(filePath):
        cosmicData = init.PD.read_csv(filePath, sep=',')
        cosmicData = cosmicData[["Gene Symbol", "Entrez GeneId", "Tumour Types(Somatic)", "Tumour Types(Germline)"]]
        cosmicData = cosmicData.to_numpy()

        cosmicSet = set()
        for row in cosmicData:
            symbol = str(row[0]).strip()
            entrezID = str(row[1]).strip()
            diseaseNameSomatic = str(row[2]).strip()
            diseaseNameGermline = str(row[3]).strip()
            if not util.isNan(diseaseNameSomatic):
                cosmicSet.add(ar.CosmicRow(symbol, entrezID, diseaseNameSomatic))
            if not util.isNan(diseaseNameGermline):
                cosmicSet.add(ar.CosmicRow(symbol, entrezID, diseaseNameGermline))

        return cosmicSet
