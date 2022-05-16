from Sources import clinvar, cosmic, diseases, disgenet, hpo, humsavar, orphanet
from Mapping import obo, uniprot, hugo
from Common.init import Source


class DBContext:
    def __init__(self):
        self.disGeNet = disgenet.DisGeNet.Read()
        self.cosmic = cosmic.Cosmic.Read()
        self.clinvar = clinvar.ClinVar.Read()
        self.humsavar = humsavar.HumsaVar.Read()
        self.orphanet = orphanet.Orphanet.Read()
        self.hpo = hpo.HPO.Read()
        self.diseases = diseases.Diseases.Read()
        self.obo = obo.OBO.Read()
        self.uniprot = uniprot.Uniprot.Read()
        self.hugo = hugo.Hugo.Read()

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
