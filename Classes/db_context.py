from Sources import clinvar, cosmic, diseases, disgenet, hpo, humsavar, orphanet
from Mapping import obo, uniprot, hugo
from Common import constant


class DBContext:
    def __init__(self):
        # self.disGeNet = disgenet.DisGeNet.Read(constant.DISGENET_PATH)
        # self.cosmic = cosmic.Cosmic.Read(constant.COSMIC_PATH)
        # self.clinvar = clinvar.ClinVar.Read(constant.CLINVAR_PATH)
        # self.humsavar = humsavar.HumsaVar.Read(constant.HUMSAVAR_PATH)
        # self.orphanet = orphanet.Orphanet.Read(constant.ORPHANET_PATH)
        # self.hpoSet = hpo.HPO.Read(constant.HPO_PATH)
        # self.diseases = diseases.Diseases.Read(constant.DISEASES_PATH)
        # self.obo = obo.OBO.Read(constant.OBO_PATH)
        # self.uniprot = uniprot.Uniprot.Read(constant.UNIPROT_PATH)
        self.hugo = hugo.Hugo.Read(constant.HUGO_PATH)