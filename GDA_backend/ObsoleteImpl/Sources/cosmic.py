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

from GDA_backend.Classes.annotation_models import CosmicRow
from GDA_backend.Common.constants import COSMIC_PATH
from GDA_backend.Common.init import pd, OrderedSet
from GDA_backend.Common.util import CheckNan


class Cosmic:
    @staticmethod
    def Read(filePath=COSMIC_PATH):
        cosmicData = pd.read_csv(filePath, sep=',', dtype=str)
        cosmicData = cosmicData[["Gene Symbol", "Entrez GeneId", "Tumour Types(Somatic)", "Tumour Types(Germline)"]]
        cosmicData = cosmicData.to_numpy()

        cosmicSet = OrderedSet()
        for row in cosmicData:
            symbol = CheckNan(row[0])
            entrezID = CheckNan(row[1])
            diseaseNameSomatic = CheckNan(row[2])
            diseaseNameGermline = CheckNan(row[3])
            if diseaseNameSomatic is not None:
                cosmicSet.add(CosmicRow(symbol, entrezID, diseaseNameSomatic))
            if diseaseNameGermline is not None:
                cosmicSet.add(CosmicRow(symbol, entrezID, diseaseNameGermline))

        return cosmicSet
