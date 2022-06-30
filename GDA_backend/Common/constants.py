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

__filenamesJSON = ImportDataFilenamesJson("data_filenames.json")
__FILENAMES_JSON = __filenamesJSON if __filenamesJSON is not None else {}

__DATA_DIRECTORY = __FILENAMES_JSON["DATA_DIRECTORY"] if "DATA_DIRECTORY" in __FILENAMES_JSON else "./Data"
# Sources
__CLINVAR_FILE = __FILENAMES_JSON["CLINVAR"] if "CLINVAR" in __FILENAMES_JSON else "clinvar.txt"
__COSMIC_FILE = __FILENAMES_JSON["COSMIC"] if "COSMIC" in __FILENAMES_JSON else "cosmic.csv"
__DISEASES_FILE = __FILENAMES_JSON["DISEASES"] if "DISEASES" in __FILENAMES_JSON else "diseases.tsv"
__DISGENET_FILE = __FILENAMES_JSON["DISGENET"] if "DISGENET" in __FILENAMES_JSON else "disgenet.tsv"
__HPO_FILE = __FILENAMES_JSON["HPO"] if "HPO" in __FILENAMES_JSON else "hpo.txt"
__HUMSAVAR_FILE = __FILENAMES_JSON["HUMSAVAR"] if "HUMSAVAR" in __FILENAMES_JSON else "humsavar.txt"
__ORPHANET_FILE = __FILENAMES_JSON["ORPHANET"] if "ORPHANET" in __FILENAMES_JSON else "orphanet.xml"

# Mapping
__RGD_OBO_FILE = __FILENAMES_JSON["RGD_OBO"] if "RGD_OBO" in __FILENAMES_JSON else "rgd.txt"
__OBO_FILE = __FILENAMES_JSON["OBO"] if "OBO" in __FILENAMES_JSON else "obo.txt"
__UNIPROT_FILE = __FILENAMES_JSON["UNIPROT"] if "UNIPROT" in __FILENAMES_JSON else "uniprot.dat"
__HUGO_FILE = __FILENAMES_JSON["HUGO"] if "HUGO" in __FILENAMES_JSON else "hugo.txt"
__ORPHANET_XREF_FILE = __FILENAMES_JSON["ORPHANET_XREF"] if "ORPHANET_XREF" in __FILENAMES_JSON else "orphanet_xref.xml"

# Sources
CLINVAR_PATH = os.path.join(__DATA_DIRECTORY, __CLINVAR_FILE)
COSMIC_PATH = os.path.join(__DATA_DIRECTORY, __COSMIC_FILE)
DISEASES_PATH = os.path.join(__DATA_DIRECTORY, __DISEASES_FILE)
DISGENET_PATH = os.path.join(__DATA_DIRECTORY, __DISGENET_FILE)
HPO_PATH = os.path.join(__DATA_DIRECTORY, __HPO_FILE)
HUMSAVAR_PATH = os.path.join(__DATA_DIRECTORY, __HUMSAVAR_FILE)
ORPHANET_PATH = os.path.join(__DATA_DIRECTORY, __ORPHANET_FILE)

# Mapping
RGD_OBO_PATH = os.path.join(__DATA_DIRECTORY, __RGD_OBO_FILE)
OBO_PATH = os.path.join(__DATA_DIRECTORY, __OBO_FILE)
UNIPROT_PATH = os.path.join(__DATA_DIRECTORY, __UNIPROT_FILE)
HUGO_PATH = os.path.join(__DATA_DIRECTORY, __HUGO_FILE)
ORPHANET_XREF_PATH = os.path.join(__DATA_DIRECTORY, __ORPHANET_XREF_FILE)

# Search Engine
API_KEY = "1"  # TODO: implement guid api key creation
COLLECTION_NAME_DOID = "DOID"
QUERY_BY_DOID = "diseaseName, definition"

# Storage
__STORAGE_DIRECTORY = "./Storage"
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
