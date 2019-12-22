# -*- coding: utf-8 -*-
from paths import *
from collections import Counter
import copy
import fnmatch
import shutil
import getpass
import sys

##################################################
meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1

paths = Paths(meleti, mel_type, company_name)
kt_map = load_json(paths.kt_info_path)
kt = NamesAndLists(kt_map)

##################################################


dir_compare(paths.localdata, paths.paradosidata, match='.xml')
