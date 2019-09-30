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


############################################

# clearlocalpath = paths.localdata
#
#
# def counter():
#     astenot = []
#     astik = []
#     astota = []
#     asttom = []
#     bld = []
#     cbound = []
#     dbound = []
#     oik = []
#     poi = []
#     pre_coastline = []
#     pre_fbound = []
#     pst = []
#     rbound = []
#     roads = []
#     fbound = []
#     eas = []
#     vst = []
#
#     kt_map = {"ASTENOT": astenot,
#               "ASTIK": astik,
#               "ASTOTA": astota,
#               "ASTTOM": asttom,
#               "BLD": bld,
#               "CBOUND": cbound,
#               "DBOUND": dbound,
#               "OIK": oik,
#               "POI": poi,
#               "FBOUND": fbound,
#               "PRE_COASTLINE": pre_coastline,
#               "PRE_FBOUND": pre_fbound,
#               "PST": pst,
#               "ROADS": roads,
#               "EAS": eas,
#               "VST": vst,
#               "RBOUND": rbound}
#
#     for rootDir, subdirs, filenames in os.walk(clearlocalpath):
#         for filename in fnmatch.filter(filenames, '*shp'):
#             kt_map[os.path.splitext(filename)[0]].append(os.path.join(rootDir, filename))
#
#     # for i in kt_map:
#     #     if len(kt_map[i]):
#     #         print('{} --> {}'.format(i, len(kt_map[i])))
#
#     no_data = []
#
#     print("ASTENOT  -  {}".format(len(kt_map['ASTENOT']))) if kt_map['ASTENOT'] else "ASTENOT - No Data" and no_data.append('ASTENOT')
#     print("ASTIK    -  {}".format(len(kt_map['ASTIK']))) if kt_map['ASTIK'] else no_data.append('ASTIK')
#     print("ASTOTA   -  {}".format(len(kt_map['ASTOTA']))) if kt_map['ASTOTA'] else no_data.append('ASTOTA')
#     print("ASTTOM   -  {}".format(len(kt_map['ASTTOM']))) if kt_map['ASTTOM'] else no_data.append('ASTTOM')
#     print("BLD      -  {}".format(len(kt_map['BLD']))) if kt_map['BLD'] else no_data.append('BLD')
#     print("PST      -  {}".format(len(kt_map['PST']))) if kt_map['PST'] else no_data.append('PST')
#     print("VST      -  {}".format(len(kt_map['VST']))) if kt_map['VST'] else no_data.append('VST')
#     print("ROADS    -  {}".format(len(kt_map['ROADS']))) if kt_map['ROADS'] else no_data.append('ROADS')
#     print("FBOUND   -  {}".format(len(kt_map['FBOUND']))) if kt_map['FBOUND'] else no_data.append('FBOUND')
#
#     print("OIK      -  {}".format(len(kt_map['OIK']))) if kt_map['OIK'] else "OIK - No Data" and no_data.append('OIK')
#     print("POI      -  {}".format(len(kt_map['POI']))) if kt_map['POI'] else no_data.append('POI')
#
#     print("RBOUND   -  {}".format(len(kt_map['RBOUND']))) if kt_map['RBOUND'] else no_data.append('RBOUND')
#     print("DBOUND   -  {}".format(len(kt_map['DBOUND']))) if kt_map['DBOUND'] else no_data.append('DBOUND')
#     print("CBOUND   -  {}".format(len(kt_map['CBOUND']))) if kt_map['CBOUND'] else no_data.append('CBOUND')
#     print("EAS      -  {}".format(len(kt_map['EAS']))) if kt_map['EAS'] else no_data.append('EAS')
#
#     print("PRE_COASTLINE  -  PRE_COASTLINE".format(len(kt_map['PRE_COASTLINE']))) if kt_map['PRE_COASTLINE'] else no_data.append('PRE_COASTLINE')
#     print("PRE_FBOUND  -  PRE_FBOUND".format(len(kt_map['PRE_FBOUND']))) if kt_map['PRE_FBOUND'] else no_data.append('PRE_FBOUND')
#
#     print(no_data)
#
#
# counter()


############################################

# def build_structure():
#     # for rootDir, subdirs, filenames in os.walk(repo):
#     #     for filename in filenames:
#     #         # for filename in fnmatch.filter(filenames, '*shp'):
#     #         #     kt_map[os.path.splitext(filename)[0]].append(os.path.join(rootDir, filename))
#     #
#     #         print(os.path.join(rootDir, filename))
#
#     # for dirpath, dirnames, filenames in os.walk(repo):
#     #     structure = os.path.join(target, dirpath[len(repo):])
#     #     print(structure)
#     #     # if not os.path.isdir(structure):
#     #     #     os.mkdir(structure)
#     #     # else:
#     #     #     print("Folder does already exits!")
#
#     # def ig_f(_dir, files):
#     #     return [f for f in files if os.path.isfile(os.path.join(_dir, f))]
#
#     # try:
#     #     shutil.copytree(repo, target)
#     # except WindowsError:
#     #     print('"{}" directory already exists'.format(target))


# src = r"C:\Python27\ArcGIS10.1\Lib\site-packages\ktima"
# dst = [users, 'aznavouridis.k', 'Desktop', 'kt_build', 'code']
#
# for rootDir, subdirs, filenames in os.walk(src):
#     for filename in fnmatch.filter(filenames, '*py'):
#         inpath = os.path.join(rootDir, filename)
#         out = dst + inpath.split('\\')[6:]
#         outpath = cp(out)
#         c_copy(inpath, outpath)
#
# toolboxes = ["A) General",
#              "B) Check",
#              "C) Fix",
#              "D) Create"]
#
# for rootDir, subdirs, filenames in os.walk(src):
#     for filename in fnmatch.filter(filenames, '*py'):
#         basename = os.path.splitext(filename)[0]
#         if basename in toolboxes:
#             inpath = os.path.join(rootDir, filename)
#             out = dst + inpath.split('\\')[6:-1]
#             out.append('{}.pyt'.format(basename))
#             outpath = cp(out)
#             c_copy(inpath, outpath)
#         else:
#             inpath = os.path.join(rootDir, filename)
#             out = dst + inpath.split('\\')[6:]
#             outpath = cp(out)
#             c_copy(inpath, outpath)
#
#
#
#
# for rootDir, subdirs, filenames in os.walk(src):
#     for filename in fnmatch.filter(filenames, '*py'):
#         inpath = os.path.join(rootDir, filename)
#         out = dst + inpath.split('\\')[6:]
#         outpath = cp(out)
#
#         if __action == 'push':
#             c_copy(inpath, outpath)
#         else:
#             c_copy(outpath, inpath)
#

