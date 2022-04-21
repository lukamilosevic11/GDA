from Sources import clinvar, cosmic, diseases, disgenet, hpo, humsavar, orphanet
from Mapping import obo, uniprot, hugo
from Common import constants


class DBContext:
    def __init__(self):
        self.disGeNet = disgenet.DisGeNet.Read(constants.DISGENET_PATH)
        self.cosmic = cosmic.Cosmic.Read(constants.COSMIC_PATH)
        self.clinvar = clinvar.ClinVar.Read(constants.CLINVAR_PATH)
        self.humsavar = humsavar.HumsaVar.Read(constants.HUMSAVAR_PATH)
        self.orphanet = orphanet.Orphanet.Read(constants.ORPHANET_PATH)
        self.hpoSet = hpo.HPO.Read(constants.HPO_PATH)
        self.diseases = diseases.Diseases.Read(constants.DISEASES_PATH)
        self.obo = obo.OBO.Read(constants.OBO_PATH)
        self.uniprot = uniprot.Uniprot.Read(constants.UNIPROT_PATH)
        self.hugo = hugo.Hugo.Read(constants.HUGO_PATH)
