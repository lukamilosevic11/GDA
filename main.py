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

from Sources import clinvar, cosmic, diseases, disgenet, hpo, humsavar, orphanet
from common import constant, util

def main():
    clinvarSet = clinvar.ClinVar.Read(constant.CLINVAR_PATH)
    cosmicSet = cosmic.Cosmic.Read(constant.COSMIC_PATH)
    diseasesSet = diseases.Diseases.Read(constant.DISEASES_PATH)
    disGeNetSet = disgenet.DisGeNet.Read(constant.DISGENET_PATH)
    hpoSet = hpo.HPO.Read(constant.HPO_PATH)
    humsavarSet = humsavar.HumsaVar.Read(constant.HUMSAVAR_PATH)
    orphanetSet = orphanet.Orphanet.Read(constant.ORPHANET_PATH)

    # util.printSet(clinvarSet)

    # util.printSet(cosmicSet)

    # util.printSet(diseasesSet)
    # util.writeSetToFile("./Results/tmp.txt", diseasesSet)

    # util.printSet(disGeNetSet)

    # util.printSet(hpoSet)

    # util.printSet(humsavarSet)

    util.printSet(orphanetSet)
    # util.writeSetToFile("./Results/tmp.txt", orphanetSet)


if __name__ == '__main__':
    main()
