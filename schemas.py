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


# MODES
KTIMA_MODE = 'ktima'
STANDALONE_MODE = 'standalone'

# GEODATABASES
KTIMA_GDB = 'ktima.gdb'
STANDALONE_GDB = 'standalone.gdb'

# COMPANIES
c_NA = 'NAMA'
c_2P = '2KP'

# GOOGLE DRIVE MAPPING LETTERS
gd = {'aznavouridis.k': 'D',
      'user1': 'C',
      'kazna': 'D'}

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
temp2kp = '!--2KP_TEMP--'

# USER AND DRIVE LETTER MAPPING FOR EACH USER
user = getpass.getuser()
ktl = load_json(cp([users, user, 'paths.json']))


class LookUpInfo:
    """
    This class contains all information needed for the core functions.
    It takes as parameters two dictionaries and creates attributes
    of strings and lists
    """

    def __init__(self, info, naming):
        """
        :param info: **dict**
            Dictionary containing all information of the project.
        :param naming: **dict**
            Dictionary containing naming schemas of the project.
        """
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

        self.oria_etairias = '{}_ORIA_{}'.format(self.meleti.replace('-', '_'),
                                                 self.company_name)
