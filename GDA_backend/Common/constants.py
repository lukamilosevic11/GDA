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

from GDA_backend.Common.init import os
from GDA_backend.Common.util import ImportDataFilenamesJson

__STORAGE_DIRECTORY = os.path.abspath("./GDA_backend/Storage") if os.getcwd().split('/')[-1] == "GDA" \
    else os.path.abspath("../GDA_backend/Storage")

__DATA_FILENAMES_PATH = os.path.join(__STORAGE_DIRECTORY, "data_filenames.json")

__filenamesJSON = ImportDataFilenamesJson(__DATA_FILENAMES_PATH)
__FILENAMES_JSON = __filenamesJSON if __filenamesJSON is not None else {}

__DATA_DIRECTORY = os.path.abspath("./GDA_backend/Data") \
    if os.getcwd().split('/')[-1] == "GDA" else os.path.abspath("../GDA_backend/Data")

__DATA_DIRECTORY_STORAGE = os.path.join(__STORAGE_DIRECTORY, __FILENAMES_JSON["DATA_DIRECTORY"]) \
    if "DATA_DIRECTORY" in __FILENAMES_JSON else __STORAGE_DIRECTORY


def GetPath(sourceName, fileName):
    if sourceName in __FILENAMES_JSON and os.path.exists(
            os.path.join(__DATA_DIRECTORY_STORAGE, __FILENAMES_JSON[sourceName])):
        return os.path.join(__DATA_DIRECTORY_STORAGE, __FILENAMES_JSON[sourceName])
    return os.path.join(__DATA_DIRECTORY, fileName)


# Sources
CLINVAR_PATH = GetPath("CLINVAR", "clinvar.txt")
COSMIC_PATH = GetPath("COSMIC", "cosmic.csv")
DISEASES_PATH = GetPath("DISEASES", "diseases.tsv")
DISGENET_PATH = GetPath("DISGENET", "disgenet.tsv")
HPO_PATH = GetPath("HPO", "hpo.txt")
HUMSAVAR_PATH = GetPath("HUMSAVAR", "humsavar.txt")
ORPHANET_PATH = GetPath("ORPHANET", "orphanet.xml")

# Mapping
RGD_OBO_PATH = GetPath("RGD_OBO", "rgd.txt")
OBO_PATH = GetPath("OBO", "obo.txt")
UNIPROT_PATH = GetPath("UNIPROT", "uniprot.dat")
HUGO_PATH = GetPath("HUGO", "hugo.txt")
ORPHANET_XREF_PATH = GetPath("ORPHANET_XREF", "orphanet_xref.xml")
ENSEMBL_ENTREZ_PATH = GetPath("ENSEMBL_ENTREZ", "ensembl_entrez.tsv")
ENSEMBL_UNIPROT_PATH = GetPath("ENSEMBL_UNIPROT", "ensembl_uniprot.tsv")

# Search Engine
if os.path.exists("api_key.txt"):
    with open("api_key.txt", "r") as file:
        API_KEY = file.readline().strip()
else:
    API_KEY = "CjRuG4L-G0yv30cj8YlntQ"

COLLECTION_NAME_DOID = "DOID"
QUERY_BY_DOID = "diseaseName, definition"

# Error
__ERROR_LOG_FILE = "error_log.txt"
ERROR_LOG_PATH = os.path.join(__STORAGE_DIRECTORY, __ERROR_LOG_FILE)

# Storage
__DISEASE_NAME_DOID_JSONL_FILE = "disease_name_doid.jsonl"
DISEASE_NAME_DOID_JSONL_PATH = os.path.join(__STORAGE_DIRECTORY, __DISEASE_NAME_DOID_JSONL_FILE)

# ANNOTATION PATH
__ANNOTATION_FILE = "annotation_file.txt"
ANNOTATION_PATH = os.path.join(__STORAGE_DIRECTORY, __ANNOTATION_FILE)

# DOID ACCURACY PATH
__DOID_ACCURACY_FILE = "doid_accuracy.txt"
DOID_ACCURACY_PATH = os.path.join(__STORAGE_DIRECTORY, __DOID_ACCURACY_FILE)

# DOID Sources
# Xref sources
DOID_SOURCE_XREF_OMIM = "Xref -> OMIM"
DOID_SOURCE_XREF_UMLS = "Xref -> UMLS"
DOID_SOURCE_XREF_MESH = "Xref -> MeSH"
DOID_SOURCE_XREF_GARD = "Xref -> GARD"
DOID_SOURCE_XREF_MEDDRA = "Xref -> MedDRA"
DOID_SOURCE_XREF_ICD10 = "Xref -> ICD-10"

DOID_SOURCE_SEARCH_ENGINE = "DiseaseName -> Typesense"
DOID_SOURCE_FROZEN_SET = "DiseaseName -> Frozenset"
DOID_SOURCE_DATABASE = "Database"

# Annotation file header
ANNOTATION_FILE_HEADER = "Gene Symbol\tEntrez ID\tUniprot ID\tEnsembl ID\tDOID\tSource\tDisease Name\tDOID Source"
