# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#

# This module is responsible for updating the status of the project.

from ktima.logger import *
from ktima.cust_arc import *


warning_counter = 0


def check_ktima_version():
    """
    Checks if the local ktima version is up to date.

    :return: Nothing
    """

    global warning_counter

    if local_ktima_version != server_ktima_version and warning_counter < 4:
        pm('\n! There is an updated "ktima" version !')
        pm('Your release : {}'.format(local_ktima_version))
        pm('Newer release: {}\n'.format(server_ktima_version))
        warning_counter += 1
    else:
        pass


class KTStatus:
    """
    Status can check update and show the status of the working project.

    Attributes
    ----------
    - mode: ktima mode which the USER is working (ktima or standalone)
    - meleti: meleti of the project
    - otas: otas the USER has selected. Mode-dependent
    - status_path: path for the KT_Status.json file

    Methods
    -------
    - check
    - update
    - show
    """

    def __init__(self, meleti, mode, otas):
        """
        :param meleti: str
            Meleti.
        :param mode: str
            Ktima mode.
        :param otas: list
            List of otas the USER is working with.
        """

        self.mode = mode
        self.meleti = meleti
        self.otas = otas
        self.status_path = cp([meleti, inputdata, docs_i, json_status])

    def check(self, shape_type, shape):
        """
        Checks current status.

        :param shape_type: str
            Category inside json file.
        :param shape: str
            Category inside json file.
        :return: any
            The functions can return eiher a boolean or list or str or number.
        """

        data = load_json(self.status_path)

        status = data[self.mode][shape_type][shape]

        return status

    def update(self, shape_type, shape, status):
        """
        Updates current status

        :param shape_type: str
            Category inside json file.
        :param shape: str
            Category inside json file.
        :param status: any
            boolean or list or str or number.
        :return: Nothing
        """

        data = load_json(self.status_path)

        data[self.mode][shape_type][shape] = status

        write_json(self.status_path, data)

    def show(self):
        """
        Prints predefined message of the current status
        :return: Nothing
        """

        data = load_json(self.status_path)

        pm("\nMeleti: {}  --  {}".format(self.meleti, self.mode.upper()))

        if self.mode == STANDALONE_MODE:
            pm("\nOTA : {}".format('-'.join(self.otas)))

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
