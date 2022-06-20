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

__DATA_DIRECTORY = "./Data/"
# Sources
__CLINVAR_FILE = "gene_condition_source_id.txt"
__COSMIC_FILE = "cancer_gene_census.csv"
__DISEASES_FILE = "human_disease_textmining_filtered.tsv"
__DISGENET_FILE = "curated_gene_disease_associations.tsv"
__HPO_FILE = "genes_to_phenotype.txt"
__HUMSAVAR_FILE = "humsavar.txt"
__ORPHANET_FILE = "en_product6.xml"

# Mapping
__RGD_OBO_FILE = "RDO.obo.txt"
__OBO_FILE = "doid.obo.txt"
__UNIPROT_FILE = "HUMAN_9606_idmapping.dat"
__HUGO_FILE = "hgnc_complete_set.txt"
__ORPHANET_XREF_FILE = "en_product1.xml"

# TODO: implement with os.path and maybe reading from some json file
# Sources
CLINVAR_PATH = __DATA_DIRECTORY + __CLINVAR_FILE
COSMIC_PATH = __DATA_DIRECTORY + __COSMIC_FILE
DISEASES_PATH = __DATA_DIRECTORY + __DISEASES_FILE
DISGENET_PATH = __DATA_DIRECTORY + __DISGENET_FILE
HPO_PATH = __DATA_DIRECTORY + __HPO_FILE
HUMSAVAR_PATH = __DATA_DIRECTORY + __HUMSAVAR_FILE
ORPHANET_PATH = __DATA_DIRECTORY + __ORPHANET_FILE

# Mapping
RGD_OBO_PATH = __DATA_DIRECTORY + __RGD_OBO_FILE
OBO_PATH = __DATA_DIRECTORY + __OBO_FILE
UNIPROT_PATH = __DATA_DIRECTORY + __UNIPROT_FILE
HUGO_PATH = __DATA_DIRECTORY + __HUGO_FILE
ORPHANET_XREF_PATH = __DATA_DIRECTORY + __ORPHANET_XREF_FILE

# Search Engine
API_KEY = "1"  # TODO: implement guid api key creation
COLLECTION_NAME_DOID = "DOID"
QUERY_BY_DOID = "diseaseName, definition"

# Storage
__STORAGE_DIRECTORY = "./Storage/"
__DISEASE_NAME_DOID_JSONL_FILE = "diseaseNameDoid.jsonl"
DISEASE_NAME_DOID_JSONL_PATH = __STORAGE_DIRECTORY + __DISEASE_NAME_DOID_JSONL_FILE

MAX_JACCARD_INDEX = 1.0

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
