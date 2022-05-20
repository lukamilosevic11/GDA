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
__OBO_FILE = "RDO.obo.txt"
__UNIPROT_FILE = "HUMAN_9606_idmapping.dat"
__HUGO_FILE = "hgnc_complete_set.txt"

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
OBO_PATH = __DATA_DIRECTORY + __OBO_FILE
UNIPROT_PATH = __DATA_DIRECTORY + __UNIPROT_FILE
HUGO_PATH = __DATA_DIRECTORY + __HUGO_FILE

# Search Engine
API_KEY = "1"
COLLECTION_NAME_DOID = "DOID"
QUERY_BY_DOID = "diseaseName"

# Storage
__STORAGE_DIRECTORY = "./Storage/"
__DISEASE_NAME_DOID_JSONL_FILE = "diseaseNameDoid.jsonl"
DISEASE_NAME_DOID_JSONL_PATH = __STORAGE_DIRECTORY + __DISEASE_NAME_DOID_JSONL_FILE
