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

import numpy as NP
import pandas as PD
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
import xml.etree.ElementTree as ET
import multiprocessing
import json
import typesense
import time
import concurrent.futures
import string
from pronto import Ontology
from time import perf_counter
from threading import Thread
from enum import Enum


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
