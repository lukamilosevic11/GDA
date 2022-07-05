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

import copy
import json
import multiprocessing
import nltk
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
import numpy as np
import pandas as pd
import re
import os
import string
import time
import typesense
import xml.etree.ElementTree as et
from collections import OrderedDict
from tabulate import tabulate
from ordered_set import OrderedSet
from enum import Enum, IntEnum
from functools import partial
from itertools import permutations
from pronto import Ontology
from threading import Thread, Lock
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, TextColumn, BarColumn, TaskProgressColumn, \
    TimeRemainingColumn, MofNCompleteColumn


class Xref(IntEnum):
    UMLS = 1
    MeSH = 2
    GARD = 3
    MedDRA = 4
    OMIM = 5
    ICD10 = 6


# Xrefs
XREFS_SOURCE = {
    "UMLS_CUI": Xref.UMLS,
    "MESH": Xref.MeSH,
    "MEDDRA": Xref.MedDRA,
    "ICD10CM": Xref.ICD10,
    "OMIM": Xref.OMIM,
    "GARD": Xref.GARD
}


class Attribute(Enum):
    SYMBOL = 1
    ENTREZ_ID = 2
    UNIPROT_ID = 3
    ENSEMBL_ID = 4
    DOID = 5
    SOURCE = 6
    DISEASE_NAME = 7


class Source(Enum):
    DISGENET = 1
    COSMIC = 2
    CLINVAR = 3
    HUMSAVAR = 4
    ORPHANET = 5
    HPO = 6
    DISEASES = 7
    OBO = 8
    UNIPROT = 9
    HUGO = 10
    ORPHANET_XREF = 11

    @staticmethod
    def GetAllSources():
        return [Source.DISGENET, Source.COSMIC, Source.CLINVAR, Source.HUMSAVAR, Source.ORPHANET,
                Source.HPO, Source.DISEASES, Source.OBO, Source.UNIPROT, Source.HUGO, Source.ORPHANET_XREF]

    @staticmethod
    def GetSourcesForParsing():
        return [Source.DISGENET, Source.COSMIC, Source.CLINVAR, Source.HUMSAVAR, Source.ORPHANET, Source.HPO,
                Source.DISEASES]

    @staticmethod
    def GetSourceName(source):
        if source is Source.DISGENET:
            return "DisGeNet"
        elif source is Source.COSMIC:
            return "Cosmic"
        elif source is Source.CLINVAR:
            return "ClinVar"
        elif source is Source.HUMSAVAR:
            return "HumsaVar"
        elif source is Source.ORPHANET:
            return "Orphanet"
        elif source is Source.HPO:
            return "HPO"
        elif source is Source.DISEASES:
            return "Diseases"
        elif source is Source.OBO:
            return "OBO"
        elif source is Source.UNIPROT:
            return "Uniprot"
        elif source is Source.HUGO:
            return "Hugo"
        elif source is Source.ORPHANET_XREF:
            return "Orphanet Xref"