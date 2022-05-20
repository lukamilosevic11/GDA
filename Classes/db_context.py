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

from Common.init import Source
from Mapping.hugo import Hugo
from Mapping.obo import OBO
from Mapping.uniprot import Uniprot
from Sources.clinvar import ClinVar
from Sources.cosmic import Cosmic
from Sources.diseases import Diseases
from Sources.disgenet import DisGeNet
from Sources.hpo import HPO
from Sources.humsavar import HumsaVar
from Sources.orphanet import Orphanet


class DBContext:
    def __init__(self):
        self.disGeNet = DisGeNet.Read()
        self.cosmic = Cosmic.Read()
        self.clinvar = ClinVar.Read()
        self.humsavar = HumsaVar.Read()
        self.orphanet = Orphanet.Read()
        self.hpo = HPO.Read()
        self.diseases = Diseases.Read()
        self.obo = OBO.Read()
        self.uniprot = Uniprot.Read()
        self.hugo = Hugo.Read()

    def GetDatabaseBySource(self, source):
        if source is Source.DISGENET:
            return self.disGeNet
        elif source is Source.COSMIC:
            return self.cosmic
        elif source is Source.CLINVAR:
            return self.clinvar
        elif source is Source.HUMSAVAR:
            return self.humsavar
        elif source is Source.ORPHANET:
            return self.orphanet
        elif source is Source.HPO:
            return self.hpo
        elif source is Source.DISEASES:
            return self.diseases
        elif source is Source.OBO:
            return self.obo
        elif source is Source.UNIPROT:
            return self.uniprot
        elif source is Source.HUGO:
            return self.hugo
