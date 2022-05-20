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

from Classes.annotation_row import OBORow
from Common.constants import OBO_PATH
from Common.init import Ontology, multiprocessing


class OBO:
    @staticmethod
    def Read(filePath=OBO_PATH):
        oboData = Ontology(filePath, threads=multiprocessing.cpu_count())
        oboSet = set()

        for term in oboData.terms():
            if term.obsolete:
                continue
            doid = term.id.strip()
            diseaseName = term.name.strip()
            synonyms = term.synonyms
            parentDoids = term.superclasses().to_set()
            oboSet.add(OBORow(doid, diseaseName, synonyms, parentDoids))

        return oboSet
