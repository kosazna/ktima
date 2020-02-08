# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from logger import *

json_status = {'company': 'KT_Status_company.json',
               'standalone': 'KT_Status_standalone.json'}


class Status:

    def __init__(self, meleti, mode):
        self.mode = mode
        self.meleti = meleti
        self.status_path = cp([meleti, inputdata, docs_i, json_status[mode]])

    def check(self, shape_type, shape):
        data = load_json(self.status_path)

        status = data[shape_type][shape]

        return status

    def update(self, shape_type, shape, status):
        data = load_json(self.status_path)

        data[shape_type][shape] = status

        write_json(self.status_path, data)

    def show(self):
        data = load_json(self.status_path)

        pm("\nMeleti: {}  --  {}" .format(self.meleti, self.mode.upper()))

        pm("\nGeometry Status")
        pm("---------------------")
        pm("FBOUND  -  Geometry Problems : {}".format(data["FBOUND_GEOMETRY"]["OTA"])) if data["FBOUND_GEOMETRY"]["PROBS"] else pm(
            "FBOUND  -  Geometry OK")
        pm("Check Date : {}\n".format(data["FBOUND_GEOMETRY"]["CD"]))
        pm("SHAPES  -  Geometry Problems : {}".format(data["SHAPES_GEOMETRY"]["OTA"])) if data["SHAPES_GEOMETRY"]["PROBS"] else pm(
            "SHAPES  -  Geometry OK")
        pm("Check Date : {}\n".format(data["SHAPES_GEOMETRY"]["CD"]))

        pm("\nMerging Status")
        pm("---------------------")
        pm("ASTENOT  -  Merged") if data["SHAPE"]["ASTENOT"] else pm("ASTENOT  -  Not Merged")
        pm("ASTIK    -  Merged") if data["SHAPE"]["ASTIK"] else pm("ASTIK    -  Not Merged")
        pm("ASTOTA   -  Merged") if data["SHAPE"]["ASTOTA"] else pm("ASTOTA   -  Not Merged")
        pm("ASTTOM   -  Merged") if data["SHAPE"]["ASTTOM"] else pm("ASTTOM   -  Not Merged")
        pm("BLD      -  Merged") if data["SHAPE"]["BLD"] else pm("BLD      -  Not Merged")
        pm("DBOUND   -  Merged") if data["SHAPE"]["DBOUND"] else pm("DBOUND   -  Not Merged")
        pm("FBOUND   -  Merged") if data["SHAPE"]["FBOUND"] else pm("FBOUND   -  Not Merged")
        pm("PST      -  Merged") if data["SHAPE"]["PST"] else pm("PST      -  Not Merged")
        pm("ROADS    -  Merged") if data["SHAPE"]["ROADS"] else pm("ROADS    -  Not Merged")
        pm("iROADS   -  Merged\n") if data["SHAPE"]["iROADS"] else pm("iROADS   -  Not Merged\n")

        pm("\nExports")
        pm("---------------------")
        pm("FBOUND  :  {}".format(data["EXPORTED"]["FBOUND_ED"]))
        pm("ROADS   :  {}\n".format(data["EXPORTED"]["ROADS_ED"]))

        pm("\nOverlaps")
        pm("---------------------")
        pm("Checked with : {}".format(data["OVERLAPS"]["DECIMALS"]))
        pm("Check Date : {}\n".format(data["OVERLAPS"]["CD"]))
        pm("ASTTOM  -  [ {} ]".format(data["OVERLAPS"]["ASTTOM"]))
        pm("ASTENOT -  [ {} ]".format(data["OVERLAPS"]["ASTENOT"]))
        pm("PST     -  [ {} ]\n".format(data["OVERLAPS"]["PST"]))
        pm("Wrong KAEK (ASTENOT_ASTTOM) -  [ {} ]".format(data["WRONG_KAEK"]["ASTENOT_ASTTOM"]))
        pm("Wrong KAEK (PST_ASTENOT)    -  [ {} ]\n".format(data["WRONG_KAEK"]["PST_ASTENOT"]))

        pm("\nRoads Intersections")
        pm("---------------------")
        pm("ALL    -  [ {} ]".format(data["ROADS"]["ALL"]))
        pm("PROBS  -  [ {} ]\n".format(data["ROADS"]["PROBS"]))
        pm("Check Date : {} \n".format(data["ROADS"]["CD"]))

        pm("\nProblems")
        pm("---------------------")
        pm("BLD    - [ {} ]".format(data["BLD"]["PROBS"]))
        pm("Check Date : {} \n".format(data["BLD"]["CD"]))
        pm("DBOUND - [ {} ]".format(data["DBOUND"]["PROBS"]))
        pm("Check Date : {} \n\n".format(data["DBOUND"]["CD"]))
