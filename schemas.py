# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import getpass
from cust_win import *

gd = {'aznavouridis.k': 'D',
      'user1': 'C',
      'kazna': 'D'}

build_pass = 'ktima()azna'

inputdata = "!InputData"
outputdata = "!OutputData"
geodatabases = "Geodatabases"
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

user = getpass.getuser()
ktl = load_json(cp([users, user, 'paths.json']))


class NamesAndLists:
    def __init__(self, ktdata):
        self.company_name = ktdata["company_name"]
        self.meleti = ktdata["meleti"]
        self.mel_type = ktdata["mel_type"]

        self.ota_list = ktdata["ota_list"]
        self.status_list = ktdata["status_list"]
        self.merging_list = ktdata["merging_list"]
        self.local_data_to_index_list = ktdata["local_data_to_index"]
        self.geometry_list = ktdata["geometry_list"]
        self.server_list = ktdata["server_list"]
        self.local_list = ktdata["local_list"]
        self.no_del_list = ktdata["no_del_list"]
        self.count_list = ktdata["count_list"]

        self.astenotM = ktdata["merge"]["astenot"]
        self.astikM = ktdata["merge"]["astik"]
        self.astotaM = ktdata["merge"]["astota"]
        self.asttomM = ktdata["merge"]["asttom"]
        self.bldM = ktdata["merge"]["bld"]
        self.dboundM = ktdata["merge"]["dbound"]
        self.fboundM = ktdata["merge"]["fbound"]
        self.pstM = ktdata["merge"]["pst"]
        self.roadsM = ktdata["merge"]["roads"]

        self.astenotU = ktdata["union"]["astenot"]
        self.astikU = ktdata["union"]["astik"]
        self.astotaU = ktdata["union"]["astota"]
        self.asttomU = ktdata["union"]["asttom"]
        self.bldU = ktdata["union"]["bld"]
        self.dboundU = ktdata["union"]["dbound"]
        self.fboundU = ktdata["union"]["fbound"]
        self.pstU = ktdata["union"]["pst"]
        self.roadsU = ktdata["union"]["roads"]

        self.pst_geom = ktdata["geometry"]["pst"]
        self.fbound_geom = ktdata["geometry"]["fbound"]

        self.p_pst_astenot = ktdata["probs"]["pst_astenot"]
        self.p_astenot_asttom = ktdata["probs"]["astenot_asttom"]
        self.p_geometry_kaek = ktdata["probs"]["geometry_kaek"]
        self.p_geometry_ota = ktdata["probs"]["geometry_ota"]
        self.p_roads = ktdata["probs"]["roads"]
        self.p_dbound = ktdata["probs"]["dbound"]
        self.p_bld = ktdata["probs"]["bld"]
        self.p_overlaps_astenot = ktdata["probs"]["overlaps_astenot"]
        self.p_overlaps_asttom = ktdata["probs"]["overlaps_asttom"]
        self.p_overlaps_pst = ktdata["probs"]["overlaps_pst"]

        self.pst_astenot = ktdata["misc"]["pst_astenot"]
        self.astenot_asttom = ktdata["misc"]["astenot_asttom"]
        self.ek = ktdata["misc"]["ek"]
        self.temp_ek = ktdata["misc"]["temp_ek"]
        self.temp_bld = ktdata["misc"]["temp_bld"]
        self.intersections_roads = ktdata["misc"]["intersections_roads"]
        self.intersections_pst_rd = ktdata["misc"]["intersections_pst_rd"]
        self.intersections_astenot_rd = ktdata["misc"]["intersections_astenot_rd"]
        self.ek_fixed_bound = ktdata["misc"]["ek_fixed_bound"]
        self.ek_bound_reduction = ktdata["misc"]["ek_bound_reduction"]
        self.gdb_fbound_all = ktdata["misc"]["gdb_fbound_all"]
        self.fbound_all = ktdata["misc"]["fbound_all"]
        self.gdb_roads_all = ktdata["misc"]["gdb_roads_all"]
        self.roads_all = ktdata["misc"]["roads_all"]
        self.intersection_pst_fbound = ktdata["misc"]["intersection_pst_fbound"]
        self.gdb_fbound_claim = ktdata["misc"]["gdb_fbound_claim"]
        self.fbound_claim = ktdata["misc"]["fbound_claim"]
        self.diekdikisi = ktdata["misc"]["diekdikisi"]
        self.gdb_pre_fbound_all = ktdata["misc"]["gdb_pre_fbound_all"]
        self.pre_fbound_all = ktdata["misc"]["pre_fbound_all"]
        self.rd = ktdata["misc"]["rd"]
        self.pr = ktdata["misc"]["pr"]
        self.kaek_in_dbound = ktdata["misc"]["kaek_in_dbound"]
        self.kaek_in_astik = ktdata["misc"]["kaek_in_astik"]

        self.oria_etairias = '{}_ORIA_{}'.format(self.meleti.replace('-', '_'), self.company_name)
