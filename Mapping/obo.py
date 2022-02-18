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


from Classes import annotationrow as ar
from common import init


class OBO:
    @staticmethod
    def Read(filePath):
        oboData = init.Ontology(filePath, threads=init.multiprocessing.cpu_count())
        oboSet = set()

        for term in oboData.terms():
            if term.obsolete:
                continue
            doid = term.id.strip()
            diseaseName = term.name.strip()
            #TODO think about using only EXACT synonyms
            # synonyms = filter(lambda synonym: synonym.scope == "EXACT", term.synonyms)
            synonyms = term.synonyms
            parentDoids = term.superclasses().to_set()
            oboSet.add(ar.OBORow(doid, diseaseName, synonyms, parentDoids))

        return oboSet
