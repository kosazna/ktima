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
            self.tools = [Dbound, Shapes, Geometry, Roads, Bld]
        else:
            self.tools = []


###############################################################################

class Shapes(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Shapefiles"
        self.description = "Check shapefiles for overlaps and wrong KAEK"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        dekadika = arcpy.Parameter(
            displayName="Dekadika elegxou",
            name="dekadika",
            datatype="Long",
            parameterType="Required",
            direction="Input")

        params = [dekadika]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        core.check[core.kt.mode].shapes(params[0].value)

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

        for _shape in shapes:
            if _shape == "PST":
                core.check[core.kt.mode].pst_geometry()
            elif _shape == "FBOUND":
                core.check[core.kt.mode].fbound_geometry()
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
        roads = arcpy.Parameter(
            displayName="Check new ROADS",
            name="roads",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        roads.value = "false"

        params = [roads]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True
        new_roads = bool(params[0].value)

        if new_roads:
            roads = 'new'
        else:
            roads = 'old'

        core.check[core.kt.mode].roads(roads)

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

        core.check[core.kt.mode].dbound()

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

        core.check[core.kt.mode].bld()

        return
