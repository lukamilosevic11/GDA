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
from GDA_backend.Classes.sources import SourceInput
from GDA_backend.Classes.mapping import MappingInput


class DBContext:
    def __init__(self):
        self.__disGeNet = SourceInput.ReadDisGeNet()
        self.__cosmic = SourceInput.ReadCosmic()
        self.__clinvar = SourceInput.ReadClinVar()
        self.__humsavar = SourceInput.ReadHumsaVar()
        self.__orphanet = SourceInput.ReadOrphanet()
        self.__hpo = SourceInput.ReadHPO()
        self.__obo, obsoleteDOIDs = MappingInput.ReadOBO(returnObsoleteDOIDs=True)
        self.__diseases = SourceInput.ReadDiseases(obsoleteDOIDs)
        self.__uniprot = MappingInput.ReadUniProt()
        self.__hugo = MappingInput.ReadHUGO()
        self.__orphanetXref = MappingInput.ReadOrphanetXref()
        self.__ensembl = MappingInput.ReadEnsembl()

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
        elif source is Source.ENSEMBL:
            return self.__ensembl

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
        elif source is Source.ENSEMBL:
            return len(self.__ensembl)

    def GetTotalParsingLength(self):
        return len(self.__disGeNet) + len(self.__cosmic) + len(self.__clinvar) + len(self.__humsavar) + len(
            self.__orphanet) + len(self.__hpo) + len(self.__diseases)

    def GetAllSourcesLength(self):
        return sum(list(map(self.GetDatabaseLengthBySource, Source.GetAllSources())))
