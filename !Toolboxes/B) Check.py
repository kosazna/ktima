# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import arcpy
from ktima.arc import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Check"
        self.alias = "Check Shapefiles"

        # List of tool classes associated with this toolbox
        if core.get_pass():
            self.tools = [Dbound, Overlaps, Numbering, Geometry, Roads, Bld]
        else:
            self.tools = []


###############################################################################

class Overlaps(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Overlaps"
        self.description = "Check shp_list for overlaps"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        dekadika = arcpy.Parameter(
            displayName="Precision:",
            name="dekadika",
            datatype="Long",
            parameterType="Required",
            direction="Input")

        check_what = arcpy.Parameter(
            displayName="Check:",
            name="check",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        check_what.filter.list = ['ASTOTA', 'ASTENOT-ASTTOM-PST']

        params = [check_what, dekadika]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        check_what = params[0].valueAsText

        core.check_ktima_version()

        if check_what == 'ASTOTA':
            core.check.boundaries(params[1].value)
        else:
            core.check.overlaps(params[1].value)

        return


###############################################################################

class Numbering(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Numbering"
        self.description = "Check for wrong KAEK in ENOT and ENOT in TOM"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        return

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        core.check_ktima_version()
        core.check.numbering()

        return


###############################################################################

class Geometry(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Geometry"
        self.description = "Check PST and/or FBOUND geometry"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        shape = arcpy.Parameter(
            displayName="Shapefiles",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        shape.filter.list = ["PST", "FBOUND"]

        params = [shape]

        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        shape = params[0].valueAsText
        shapes = shape.split(";")

        core.check_ktima_version()

        for _shape in shapes:
            if _shape == "PST":
                core.check.pst_geometry()
            elif _shape == "FBOUND":
                core.check.fbound_geometry()
            else:
                pass

        return


###############################################################################

class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Check ROADS for intersections."
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        buffered = arcpy.Parameter(
            displayName="Check with Buffer ({}) m".format(
                core.ns.ek_bound_reduction),
            name="buffered",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        buffered.value = "false"

        params = [buffered]

        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        buffer_dist = bool(params[0].value)

        core.check_ktima_version()
        core.check.roads(check_with_buffer=buffer_dist)

        return


###############################################################################

class Dbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DBOUND"
        self.description = "Check DBOUND for missing values"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        return

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        core.check_ktima_version()
        core.check.dbound()

        return


###############################################################################

class Bld(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "BLD"
        self.description = "Check BLD for missing values"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        return

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        core.check_ktima_version()
        core.check.bld()

        return
