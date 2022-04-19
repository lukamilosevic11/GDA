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

from Classes.search_engine_client import SearchEngineClient
from Classes.db_context import DBContext
from Common.init import Attribute, Source
from Common import constant, util


def main():
    dbContext = DBContext()

    # util.printSet(dbContext.clinvar)
    tmpFilePath = "./Results/tmp.txt"
    # util.printSet(cosmicSet)

    # util.printSet(diseasesSet)
    # util.writeSetToFile("./Results/tmp.txt", diseasesSet)

    # util.printSet(disGeNetSet)

    # util.printSet(hpoSet)

    # util.printSet(humsavarSet)

    # util.printSet(orphanetSet)
    # util.writeSetToFile("./Results/tmp.txt", orphanetSet)

    # util.printSet(oboSet)
    # util.writeSetToFile("./Results/tmp.txt", oboSet)
    # util.writeJsonSetToFile("./Results/tmp.jsonl", oboSet, [Attribute.DOID, Attribute.DISEASE_NAME], Source.OBO)
    # util.writeSetToFile(tmpFilePath, dbContext.uniprot)


if __name__ == '__main__':
    main()
