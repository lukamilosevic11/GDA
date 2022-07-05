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

from GDA_backend.Common.init import Source
from GDA_backend.Mapping.hugo import Hugo
from GDA_backend.Mapping.obo import OBO
from GDA_backend.Mapping.orphanet_xref import OrphanetXref
from GDA_backend.Mapping.uniprot import Uniprot
from GDA_backend.Sources.clinvar import ClinVar
from GDA_backend.Sources.cosmic import Cosmic
from GDA_backend.Sources.diseases import Diseases
from GDA_backend.Sources.disgenet import DisGeNet
from GDA_backend.Sources.hpo import HPO
from GDA_backend.Sources.humsavar import HumsaVar
from GDA_backend.Sources.orphanet import Orphanet


class DBContext:
    def __init__(self):
        self.__disGeNet = DisGeNet.Read()
        self.__cosmic = Cosmic.Read()
        self.__clinvar = ClinVar.Read()
        self.__humsavar = HumsaVar.Read()
        self.__orphanet = Orphanet.Read()
        self.__hpo = HPO.Read()
        self.__diseases = Diseases.Read()
        self.__obo = OBO.Read()
        self.__uniprot = Uniprot.Read()
        self.__hugo = Hugo.Read()
        self.__orphanetXref = OrphanetXref.Read()
        self.__totalLength = len(self.__disGeNet) + len(self.__cosmic) + len(self.__clinvar) + len(self.__humsavar) + \
            len(self.__orphanet) + len(self.__hpo) + len(self.__diseases)

    def GetDatabaseBySource(self, source):
        if source is Source.DISGENET:
            return self.__disGeNet
        elif source is Source.COSMIC:
            return self.__cosmic
        elif source is Source.CLINVAR:
            return self.__clinvar
        elif source is Source.HUMSAVAR:
            return self.__humsavar
        elif source is Source.ORPHANET:
            return self.__orphanet
        elif source is Source.HPO:
            return self.__hpo
        elif source is Source.DISEASES:
            return self.__diseases
        elif source is Source.OBO:
            return self.__obo
        elif source is Source.UNIPROT:
            return self.__uniprot
        elif source is Source.HUGO:
            return self.__hugo
        elif source is Source.ORPHANET_XREF:
            return self.__orphanetXref

    def GetDatabaseLengthBySource(self, source):
        if source is Source.DISGENET:
            return len(self.__disGeNet)
        elif source is Source.COSMIC:
            return len(self.__cosmic)
        elif source is Source.CLINVAR:
            return len(self.__clinvar)
        elif source is Source.HUMSAVAR:
            return len(self.__humsavar)
        elif source is Source.ORPHANET:
            return len(self.__orphanet)
        elif source is Source.HPO:
            return len(self.__hpo)
        elif source is Source.DISEASES:
            return len(self.__diseases)
        elif source is Source.OBO:
            return len(self.__obo)
        elif source is Source.UNIPROT:
            return len(self.__uniprot)
        elif source is Source.HUGO:
            return len(self.__hugo)
        elif source is Source.ORPHANET_XREF:
            return len(self.__orphanetXref)

    def GetTotalParsingLength(self):
        return self.__totalLength

    def GetAllSourcesLength(self):
        return sum(list(map(self.GetDatabaseLengthBySource, Source.GetAllSources())))