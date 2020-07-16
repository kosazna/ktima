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

warning_counter = 0


def check_ktima_version():
    """
    Checks if the local ktima version is up to date.

    :return: Nothing
    """

    global warning_counter

    if local_ktima_version != server_ktima_version and warning_counter < 2:
        print('\n! There is an updated "ktima" version !')
        print('Your release : {}'.format(local_ktima_version))
        print('Newer release: {}\n'.format(server_ktima_version))
        warning_counter += 1
    else:
        pass

    return


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

        print("\nMeleti: {}  --  {}".format(self.meleti, self.mode.upper()))

        if self.mode == STANDALONE_MODE:
            print("\nOTA : {}".format('-'.join(self.otas)))

        print("\nGeometry Status")
        print("---------------------")
        print("FBOUND  -  Geometry Problems : {}".format(
            data[self.mode]["FBOUND_GEOMETRY"]["OTA"])) if \
            data[self.mode]["FBOUND_GEOMETRY"]["PROBS"] else (
            "FBOUND  -  Geometry OK")
        print("Check Date : {}\n".format(
            data[self.mode]["FBOUND_GEOMETRY"]["CD"]))
        print("SHAPES  -  Geometry Problems : {}".format(
            data[self.mode]["SHAPES_GEOMETRY"]["OTA"])) if \
            data[self.mode]["SHAPES_GEOMETRY"]["PROBS"] else (
            "SHAPES  -  Geometry OK")
        print("Check Date : {}\n".format(
            data[self.mode]["SHAPES_GEOMETRY"]["CD"]))

        print("\nMerging Status")
        print("---------------------")
        print "ASTENOT  -  Merged" if data[self.mode]["SHAPE"][
            "ASTENOT"] else (
            "ASTENOT  -  Not Merged")
        print "ASTIK    -  Merged" if data[self.mode]["SHAPE"]["ASTIK"] else (
            "ASTIK    -  Not Merged")
        print "ASTOTA   -  Merged" if data[self.mode]["SHAPE"]["ASTOTA"] else (
            "ASTOTA   -  Not Merged")
        print "ASTTOM   -  Merged" if data[self.mode]["SHAPE"]["ASTTOM"] else (
            "ASTTOM   -  Not Merged")
        print "BLD      -  Merged" if data[self.mode]["SHAPE"]["BLD"] else (
            "BLD      -  Not Merged")
        print "DBOUND   -  Merged" if data[self.mode]["SHAPE"]["DBOUND"] else (
            "DBOUND   -  Not Merged")
        print "FBOUND   -  Merged" if data[self.mode]["SHAPE"]["FBOUND"] else (
            "FBOUND   -  Not Merged")
        print "PST      -  Merged" if data[self.mode]["SHAPE"]["PST"] else (
            "PST      -  Not Merged")
        print "ROADS    -  Merged" if data[self.mode]["SHAPE"]["ROADS"] else (
            "ROADS    -  Not Merged")

        print("\nExports")
        print("---------------------")
        print("FBOUND  :  {}".format(data[self.mode]["EXPORTED"]["FBOUND_ED"]))
        print("ROADS   :  {}\n".format(data[self.mode]["EXPORTED"]["ROADS_ED"]))

        print("\nOverlaps")
        print("---------------------")
        print(
            "Checked with : {}".format(data[self.mode]["OVERLAPS"]["DECIMALS"]))
        print("Check Date : {}\n".format(data[self.mode]["OVERLAPS"]["CD"]))
        print("ASTTOM  -  [ {} ]".format(data[self.mode]["OVERLAPS"]["ASTTOM"]))
        print(
            "ASTENOT -  [ {} ]".format(data[self.mode]["OVERLAPS"]["ASTENOT"]))
        print("PST     -  [ {} ]\n".format(data[self.mode]["OVERLAPS"]["PST"]))
        print("Wrong KAEK (ASTENOT_ASTTOM) -  [ {} ]".format(
            data[self.mode]["WRONG_KAEK"]["ASTENOT_ASTTOM"]))
        print("Wrong KAEK (PST_ASTENOT)    -  [ {} ]\n".format(
            data[self.mode]["WRONG_KAEK"]["PST_ASTENOT"]))

        print("\nRoads Intersections")
        print("---------------------")
        print("ALL    -  [ {} ]".format(data[self.mode]["ROADS"]["ALL"]))
        print("PROBS  -  [ {} ]\n".format(data[self.mode]["ROADS"]["PROBS"]))
        print("Check Date : {} \n".format(data[self.mode]["ROADS"]["CD"]))

        print("\nProblems")
        print("---------------------")
        print("BLD    - [ {} ]".format(data[self.mode]["BLD"]["PROBS"]))
        print("Check Date : {} \n".format(data[self.mode]["BLD"]["CD"]))
        print("DBOUND - [ {} ]".format(data[self.mode]["DBOUND"]["PROBS"]))
        print("Check Date : {} \n\n".format(data[self.mode]["DBOUND"]["CD"]))
