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

import concurrent.futures
import json
import multiprocessing
import nltk
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import numpy as np
import pandas as pd
import re
import string
import time
import typesense
import xml.etree.ElementTree as et
from enum import Enum
from functools import partial
from itertools import permutations
from pronto import Ontology
from threading import Thread, Lock
from time import perf_counter


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

    @staticmethod
    def GetAllSources():
        return [Source.DISGENET, Source.COSMIC, Source.CLINVAR, Source.HUMSAVAR, Source.ORPHANET,
                Source.HPO, Source.DISEASES, Source.OBO, Source.UNIPROT, Source.HUGO]

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
