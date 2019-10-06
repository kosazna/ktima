# -*- coding: utf-8-sig -*-
from paths import *
import fnmatch
import shutil
import getpass

meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1

paths = Paths(meleti, mel_type, company_name)
kt_map = load_json(paths.kt_info_path)
kt = NamesAndLists(kt_map)

# for ota in kt.ota_list:
#     os.mkdir(os.path.join(paths.mdb_out, ota))



