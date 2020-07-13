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

local_ktima_version = '8.3.3'

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
gd = {'aznavouridis.k': 'D',
      'user1': 'C'}

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
ktl = load_json(cp([users, USER, json_paths]))

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
    def __init__(self, naming, mel_info):
        self.astenotM = naming["merge"]["astenot"]
        self.astikM = naming["merge"]["astik"]
        self.astotaM = naming["merge"]["astota"]
        self.asttomM = naming["merge"]["asttom"]
        self.bldM = naming["merge"]["bld"]
        self.dboundM = naming["merge"]["dbound"]
        self.fboundM = naming["merge"]["fbound"]
        self.pstM = naming["merge"]["pst"]
        self.roadsM = naming["merge"]["roads"]

        self.astenotU = naming["union"]["astenot"]
        self.astikU = naming["union"]["astik"]
        self.astotaU = naming["union"]["astota"]
        self.asttomU = naming["union"]["asttom"]
        self.bldU = naming["union"]["bld"]
        self.dboundU = naming["union"]["dbound"]
        self.fboundU = naming["union"]["fbound"]
        self.pstU = naming["union"]["pst"]
        self.roadsU = naming["union"]["roads"]

        self.pst_geom = naming["geometry"]["pst"]
        self.fbound_geom = naming["geometry"]["fbound"]

        self.p_pst_astenot = naming["probs"]["pst_astenot"]
        self.p_astenot_asttom = naming["probs"]["astenot_asttom"]
        self.p_geometry_kaek = naming["probs"]["geometry_kaek"]
        self.p_geometry_ota = naming["probs"]["geometry_ota"]
        self.p_roads = naming["probs"]["roads"]
        self.p_dbound = naming["probs"]["dbound"]
        self.p_bld = naming["probs"]["bld"]
        self.p_overlaps_astota = naming["probs"]["overlaps_astota"]
        self.p_overlaps_astenot = naming["probs"]["overlaps_astenot"]
        self.p_overlaps_asttom = naming["probs"]["overlaps_asttom"]
        self.p_overlaps_pst = naming["probs"]["overlaps_pst"]

        self.pst_astenot = naming["misc"]["pst_astenot"]
        self.astenot_asttom = naming["misc"]["astenot_asttom"]
        self.ek = naming["misc"]["ek"]
        self.temp_ek = naming["misc"]["temp_ek"]
        self.temp_bld = naming["misc"]["temp_bld"]
        self.intersections_roads = naming["misc"]["intersections_roads"]
        self.intersections_pst_rd = naming["misc"]["intersections_pst_rd"]
        self.intersections_astenot_rd = naming["misc"][
            "intersections_astenot_rd"]
        self.ek_fixed_bound = naming["misc"]["ek_fixed_bound"]
        self.ek_bound_reduction = naming["misc"]["ek_bound_reduction"]
        self.gdb_fbound_all = naming["misc"]["gdb_fbound_all"]
        self.fbound_all = naming["misc"]["fbound_all"]
        self.gdb_roads_all = naming["misc"]["gdb_roads_all"]
        self.roads_all = naming["misc"]["roads_all"]
        self.intersection_pst_fbound = naming["misc"]["intersection_pst_fbound"]
        self.gdb_fbound_claim = naming["misc"]["gdb_fbound_claim"]
        self.fbound_claim = naming["misc"]["fbound_claim"]
        self.diekdikisi = naming["misc"]["diekdikisi"]
        self.gdb_pre_fbound_all = naming["misc"]["gdb_pre_fbound_all"]
        self.pre_fbound_all = naming["misc"]["pre_fbound_all"]
        self.rd = naming["misc"]["rd"]
        self.pr = naming["misc"]["pr"]
        self.kaek_in_dbound = naming["misc"]["kaek_in_dbound"]
        self.kaek_in_astik = naming["misc"]["kaek_in_astik"]

        self.oria_etairias = '{}_ORIA_{}'.format(
            mel_info.meleti.replace('-', '_'),
            mel_info.company_name)
