# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from logger import *


class Status:

    def __init__(self, meleti, mode, otas):
        self.mode = mode
        self.meleti = meleti
        self.otas = otas
        self.status_path = cp([meleti, inputdata, docs_i, 'KT_Status.json'])

    def check(self, shape_type, shape):
        data = load_json(self.status_path)

        status = data[self.mode][shape_type][shape]

        return status

    def update(self, shape_type, shape, status):
        data = load_json(self.status_path)

        data[self.mode][shape_type][shape] = status

        write_json(self.status_path, data)

    def show(self):
        data = load_json(self.status_path)

        pm("\nMeleti: {}  --  {}".format(self.meleti, self.mode.upper()))

        if self.mode == STANDALONE_MODE:
            pm("\nOTA : {}".format(self.otas))

        pm("\nGeometry Status")
        pm("---------------------")
        pm("FBOUND  -  Geometry Problems : {}".format(
            data[self.mode]["FBOUND_GEOMETRY"]["OTA"])) if \
            data[self.mode]["FBOUND_GEOMETRY"]["PROBS"] else pm(
            "FBOUND  -  Geometry OK")
        pm("Check Date : {}\n".format(data[self.mode]["FBOUND_GEOMETRY"]["CD"]))
        pm("SHAPES  -  Geometry Problems : {}".format(
            data[self.mode]["SHAPES_GEOMETRY"]["OTA"])) if \
            data[self.mode]["SHAPES_GEOMETRY"]["PROBS"] else pm(
            "SHAPES  -  Geometry OK")
        pm("Check Date : {}\n".format(data[self.mode]["SHAPES_GEOMETRY"]["CD"]))

        pm("\nMerging Status")
        pm("---------------------")
        pm("ASTENOT  -  Merged") if data[self.mode]["SHAPE"]["ASTENOT"] else pm(
            "ASTENOT  -  Not Merged")
        pm("ASTIK    -  Merged") if data[self.mode]["SHAPE"]["ASTIK"] else pm(
            "ASTIK    -  Not Merged")
        pm("ASTOTA   -  Merged") if data[self.mode]["SHAPE"]["ASTOTA"] else pm(
            "ASTOTA   -  Not Merged")
        pm("ASTTOM   -  Merged") if data[self.mode]["SHAPE"]["ASTTOM"] else pm(
            "ASTTOM   -  Not Merged")
        pm("BLD      -  Merged") if data[self.mode]["SHAPE"]["BLD"] else pm(
            "BLD      -  Not Merged")
        pm("DBOUND   -  Merged") if data[self.mode]["SHAPE"]["DBOUND"] else pm(
            "DBOUND   -  Not Merged")
        pm("FBOUND   -  Merged") if data[self.mode]["SHAPE"]["FBOUND"] else pm(
            "FBOUND   -  Not Merged")
        pm("PST      -  Merged") if data[self.mode]["SHAPE"]["PST"] else pm(
            "PST      -  Not Merged")
        pm("ROADS    -  Merged") if data[self.mode]["SHAPE"]["ROADS"] else pm(
            "ROADS    -  Not Merged")
        pm("iROADS   -  Merged\n") if data[self.mode]["SHAPE"][
            "iROADS"] else pm("iROADS   -  Not Merged\n")

        pm("\nExports")
        pm("---------------------")
        pm("FBOUND  :  {}".format(data[self.mode]["EXPORTED"]["FBOUND_ED"]))
        pm("ROADS   :  {}\n".format(data[self.mode]["EXPORTED"]["ROADS_ED"]))

        pm("\nOverlaps")
        pm("---------------------")
        pm("Checked with : {}".format(data[self.mode]["OVERLAPS"]["DECIMALS"]))
        pm("Check Date : {}\n".format(data[self.mode]["OVERLAPS"]["CD"]))
        pm("ASTTOM  -  [ {} ]".format(data[self.mode]["OVERLAPS"]["ASTTOM"]))
        pm("ASTENOT -  [ {} ]".format(data[self.mode]["OVERLAPS"]["ASTENOT"]))
        pm("PST     -  [ {} ]\n".format(data[self.mode]["OVERLAPS"]["PST"]))
        pm("Wrong KAEK (ASTENOT_ASTTOM) -  [ {} ]".format(
            data[self.mode]["WRONG_KAEK"]["ASTENOT_ASTTOM"]))
        pm("Wrong KAEK (PST_ASTENOT)    -  [ {} ]\n".format(
            data[self.mode]["WRONG_KAEK"]["PST_ASTENOT"]))

        pm("\nRoads Intersections")
        pm("---------------------")
        pm("ALL    -  [ {} ]".format(data[self.mode]["ROADS"]["ALL"]))
        pm("PROBS  -  [ {} ]\n".format(data[self.mode]["ROADS"]["PROBS"]))
        pm("Check Date : {} \n".format(data[self.mode]["ROADS"]["CD"]))

        pm("\nProblems")
        pm("---------------------")
        pm("BLD    - [ {} ]".format(data[self.mode]["BLD"]["PROBS"]))
        pm("Check Date : {} \n".format(data[self.mode]["BLD"]["CD"]))
        pm("DBOUND - [ {} ]".format(data[self.mode]["DBOUND"]["PROBS"]))
        pm("Check Date : {} \n\n".format(data[self.mode]["DBOUND"]["CD"]))
