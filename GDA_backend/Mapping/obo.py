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

from GDA_backend.Classes.annotation_row import OBORow
from GDA_backend.Common.constants import OBO_PATH, RGD_OBO_PATH
from GDA_backend.Common.init import Ontology, multiprocessing, OrderedSet
from GDA_backend.Common.util import CheckEmpty


class OBO:
    @staticmethod
    def Read(filePathOBO=OBO_PATH, filePathRGD=RGD_OBO_PATH):
        filePaths = [filePathRGD, filePathOBO]
        oboSet = OrderedSet()

        for filePath in filePaths:
            oboData = Ontology(filePath, threads=multiprocessing.cpu_count())

            for term in oboData.terms():
                if term.obsolete:
                    continue

                doid = CheckEmpty(term.id)
                diseaseName = CheckEmpty(term.name)
                definition = CheckEmpty(term.definition)
                synonyms = term.synonyms
                parentDoids = list(term.superclasses(distance=1, with_self=False).to_set())
                xrefs = term.xrefs
                altIds = term.alternate_ids
                oboSet.add(OBORow(doid, diseaseName, synonyms, parentDoids, xrefs, altIds, definition))

        return oboSet
