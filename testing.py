from paths import *

meleti = 'KT2-11'
company_name = 'NAMA'
mel_type = 1

paths = Paths(meleti, mel_type, company_name)
ktdata = load_json(paths.kt_info_path)
kt = NamesAndLists(ktdata)


for _ in kt.status_list:
    print(_)
