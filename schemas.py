# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This modules contains all neccessary information for the project.
# User and path dictionary is defined here

import getpass
from cust_win import *

local_ktima_version = '8.5.4'

# MODES
KTIMA_MODE = 'ktima'
STANDALONE_MODE = 'standalone'

# GEODATABASES
KTIMA_GDB = 'ktima.gdb'
STANDALONE_GDB = 'standalone.gdb'
ARCHIVE_MDB = 'archive.mdb'

# COMPANIES
c_NA = 'NAMA'
c_2P = '2KP'

# GOOGLE DRIVE MAPPING LETTERS
gd = {'aznavouridis.k': 'D'}

build_pass = 'ktima()azna'

# NAMING FOLDER SCHEMA
inputdata = "!InputData"
outputdata = "!OutputData"
gdbs = "Geodatabases"
shapefiles_i = "Shapefiles"
docs_i = "Docs"
po_i = "PO"
databases_i = "Databases"
roadsold_i = "RoadsOld"
xml_i = "XML_Prototypes"
lyr_i = "LYR_Packages"
shapefiles_o = "Shapefiles"
localdata_o = "LocalData"
paradosidata_o = "ParadosiData"
paradosimdb_o = "ParadosiMDB"
users = "Users"
mdev = "! aznavouridis.k"
anakt = 'Anaktiseis'
saromena = 'Saromena'
temp2p = '!--2KP_TEMP--'

diafora = 'Diafora'
ktima_folder = 'ktima'
scripts = 'scripts'
program_files = 'Program Files (x86)'
arcgis10 = 'ArcGIS10.1'
arcgis = 'ArcGIS'
toolboxes_folder = '!Toolboxes'
desktop10 = 'Desktop10.1'
tools = 'Tools'
kt_tools = 'KT-Tools'
python_folder = 'Python27'
lib = 'Lib'
site_packages = 'site-packages'
google_drive = 'Google Drive'
work = 'Work'
ktima_version = 'ktima_8'
folder_structure = 'Folder_Structure'
file_structure = 'File_Structure'
passes = 'passes'
passes_temp = 'temp'
paratiriseis = 'paratiriseis'
desktop = 'Desktop'
logs = 'logs'

# NAMING FILE SCHEMA
txt_server_log = 'KTHMA_log.txt'
json_info = 'KT_Info.json'
json_paths = 'paths.json'
txt_log = 'KT_log.txt'
json_status = 'KT_Status.json'
json_uas = 'uas.json'
json_ipass = 'ipass.json'
json_naming = 'KT_Naming_Schema.json'
empty_shps = 'Empty_Shapefiles'

# USER AND DRIVE LETTER MAPPING FOR EACH USER
USER = getpass.getuser()
ktl = load_json(cp([users, USER, '.ktima', 'static', json_paths]))

# MOST COMMON FOLDER PATHS
temp_NA = [mdev, diafora, ktima_folder, scripts]
temp_2P = [temp2p, mdev, diafora, ktima_folder, scripts]

ktima_local = [python_folder, arcgis10, lib, site_packages, ktima_folder]
ktima_gd = [google_drive, work, ktima_folder, ktima_version]

toolboxes_local = [program_files, arcgis, desktop10, tools,
                   kt_tools]
toolboxes_ktima = [python_folder, arcgis10, lib, site_packages, ktima_folder,
                   toolboxes_folder]

build_folder_NA = [mdev, diafora, ktima_folder, folder_structure]
build_folder_2P = [temp2p, mdev, diafora, ktima_folder, folder_structure]
build_file_NA = [mdev, diafora, ktima_folder, file_structure]
build_file_2P = [temp2p, mdev, diafora, ktima_folder, file_structure]
build_json_path_NA = [mdev, diafora, ktima_folder, json_paths]
build_json_path_2P = [temp2p, mdev, diafora, ktima_folder, json_paths]


class KTInfo:
    def __init__(self, info):
        self.company_name = info.get("company_name", c_NA)
        self.meleti = info.get("meleti", 'KTx-xx')
        self.mel_type = info.get("mel_type", 1)
        self.precision = info.get("precision", 0.000001)
        self.mode = info.get("mode", KTIMA_MODE)

        self.pool = info.get("koinopraksia", {})
        self.comps = [et for et in self.pool.keys()]

        self.ota_list = info.get("ota_list", [])
        self.mel_ota_list = info.get("mel_ota_list", [])
        self.status_list = info.get("status_list", [])
        self.merging_list = info.get("merging_list", [])
        self.local_data_to_index_list = info.get("local_data_to_index",
                                                 [])
        self.geometry_list = info.get("geometry_list", [])
        self.server_list = info.get("server_list", [])
        self.local_list = info.get("local_list", [])
        self.no_del_list = info.get("no_del_list", [])
        self.count_list = info.get("count_list", [])

        self.all_ktima = info.get("all_ktima", [])


class KTNamingSchema:
    def __init__(self, mel_info):
        self.astikM = "merge_ASTIK"
        self.pstM = "merge_PST"
        self.asttomM = "merge_ASTTOM"
        self.astenotM = "merge_ASTENOT"
        self.roadsM = "merge_ROADS"
        self.astotaM = "merge_ASTOTA"
        self.fboundM = "merge_FBOUND"
        self.bldM = "merge_BLD"
        self.dboundM = "merge_DBOUND"

        self.astikU = "union_ASTIK"
        self.asttomU = "union_ASTTOM"
        self.dboundU = "union_DBOUND"
        self.roadsU = "union_ROADS"
        self.astenotU = "union_ASTENOT"
        self.fboundU = "union_FBOUND"
        self.astotaU = "union_ASTOTA"
        self.bldU = "union_BLD"
        self.pstU = "union_PST"

        self.p_overlaps_astenot = "_Overlaps_ASTENOT"
        self.p_overlaps_asttom = "_Overlaps_ASTTOM"
        self.p_overlaps_astota = "_Overlaps_ASTOTA"
        self.p_overlaps_pst = "_Overlaps_PST"

        self.p_astenot_asttom = "_Probs_ASTENOT_ASTTOM"
        self.p_pst_astenot = "_Probs_PST_ASTENOT"
        self.astenot_asttom = "ASTENOT_in_ASTTOM"
        self.pst_astenot = "PST_in_ASTENOT"

        self.p_geometry_kaek = "_Probs_GEOMETRY_KAEK"
        self.p_geometry_ota = "_Probs_GEOMETRY_OTA"
        self.pst_geom = "geometry_PST"
        self.fbound_geom = "geometry_FBOUND"
        self.eas_geom = "geometry_EAS"

        self.p_bld = "_Probs_BLD"
        self.p_dbound = "_Probs_DBOUND"
        self.temp_bld = "BLD_temp"

        self.p_roads = "_Probs_ROADS"
        self.p_roads_after_fix = "_Probs_ROADS_WithBuffer"
        self.intersections_roads_multi = "intersections_ROADS_multi"
        self.intersections_roads = "intersections_ROADS"
        self.intersections_after_fix = "intersections_ROADS_WithBuffer"
        self.ek_bound_reduction = -0.01
        self.ek_fixed_bound = "EK_Buffered"
        self.ek_check = "EK_ForCheck"
        self.ek = "EK"
        self.temp_ek = "EK_Temp"
        self.roadsM_breaked = "merge_ROADS_splitted"
        self.intersections_astenot_rd = "intersections_ASTENOT_RD"
        self.gdb_roads_all = "ROADS_IntersectionsFixed"
        self.roads_small = "ROADS_SmallSections"
        self.roads_all = "ROADS_ALL"

        self.fbound_claim = "FBOUND_Claim"
        self.diekdikisi = "Diekdikisi"
        self.gdb_fbound_claim = "gdb_FBOUND_CLAIM"
        self.gdb_fbound_all = "gdb_FBOUND_ALL"
        self.pre_fbound_all = "PRE_FBOUND_ALL"
        self.fbound_all = "FBOUND_ALL"
        self.gdb_pre_fbound_all = "gdb_PRE_FBOUND_ALL"
        self.pr = "PR"
        self.rd = "RD"
        self.kaek_in_dbound = "KAEK_IN_DBOUND"
        self.kaek_in_astik = "KAEK_IN_ASTIK"
        self.intersection_pst_fbound = "intersections_PST_FBOUND"

        self.oria_etairias = '{}_ORIA_{}'.format(
            mel_info.meleti.replace('-', '_'),
            mel_info.company_name)
