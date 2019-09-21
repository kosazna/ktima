# -*- coding: utf-8-sig -*-
from paths import *

meleti = 'KT5-22'
company_name = '2KP'
mel_type = 2

paths = Paths(meleti, mel_type, company_name)
ktdata = load_json(paths.kt_info_path)
kt = NamesAndLists(ktdata)

# for ota in kt.ota_list:
#     os.mkdir(os.path.join(paths.mdb_out, ota))

#####################################

# for _ in kt.status_list:
#     print(_)

# print(kt.__class__)

# for _ in dir(kt):
#     if '_list' not in _ and '__' not in _:
#         print('{} =
#         {}'.format(str(_), str(getattr(kt, _))))

# for k, v in vars(kt).iteritems():
#     print(k, v)
