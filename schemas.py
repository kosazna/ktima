# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import getpass
from cust_win import *

ktima_m = 'ktima'
standalone_m = 'standalone'

gd = {'aznavouridis.k': 'D',
      'user1': 'C',
      'kazna': 'D'}

build_pass = 'ktima()azna'

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

user = getpass.getuser()
ktl = load_json(cp([users, user, 'paths.json']))


class NamesAndLists:
    def __init__(self, info, naming):
        self.company_name = info.get("company_name", 'NOT_FOUND')
        self.meleti = info.get("meleti", 'NOT_FOUND')
        self.mel_type = info.get("mel_type", 'NOT_FOUND')
        self.precision = info.get("precision", 0.000001)
        self.mode = info.get("mode", ktima_m)

        self.ota_list = info.get("ota_list", 'NOT_FOUND')
        self.status_list = info.get("status_list", 'NOT_FOUND')
        self.merging_list = info.get("merging_list", 'NOT_FOUND')
        self.local_data_to_index_list = info.get("local_data_to_index",
                                                 'NOT_FOUND')
        self.geometry_list = info.get("geometry_list", 'NOT_FOUND')
        self.server_list = info.get("server_list", 'NOT_FOUND')
        self.local_list = info.get("local_list", 'NOT_FOUND')
        self.no_del_list = info.get("no_del_list", 'NOT_FOUND')
        self.count_list = info.get("count_list", 'NOT_FOUND')

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
