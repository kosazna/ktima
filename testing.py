# -*- coding: utf-8-sig -*-
from paths import *

meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1

paths = Paths(meleti, mel_type, company_name)
ktdata = load_json(paths.kt_info_path)
kt = NamesAndLists(ktdata)


# for _ in kt.status_list:
#     print(_)

# print(kt.__class__)

# for _ in dir(kt):
#     if '_list' not in _ and '__' not in _:
#         print('{} = {}'.format(str(_), str(getattr(kt, _))))


