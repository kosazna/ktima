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
import copy


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


class Shapes(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Shapefiles"
        self.description = "Check shapefiles for overlaps and wrong KAEK"
        self.canRunInBackground = False

    def getParameterInfo(self):
        dekadika = arcpy.Parameter(
            displayName="Dekadika elegxou",
            name="dekadika",
            datatype="Long",
            parameterType="Required",
            direction="Input")

        # standalone = arcpy.Parameter(
        #     displayName="Standalone check",
        #     name="Standalone Merge",
        #     datatype="Boolean",
        #     parameterType="Required",
        #     direction="Input")
        #
        # otas_to_merge = arcpy.Parameter(
        #     displayName="OTA",
        #     name="OTA",
        #     datatype="String",
        #     parameterType="Optional",
        #     direction="Input",
        #     multiValue=True)

        # if core.mxdName == core.mxdGeneralName or core.mxdName == core.mxdKtimaName:
        #     otas_values = copy.copy(core.lut.ota_list)
        #     otas_to_merge.filter.list = []
        #
        # standalone.value = "false"

        params = [dekadika]
        return params

    def updateParameters(self, params):

        # if params[1].value:
        #     otas_values = copy.copy(core.lut.ota_list)
        #     params[2].filter.list = otas_values

        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True

        # otas_to_merge = params[2].valueAsText
        # otas = otas_to_merge.split(";")
        # standalone_merge = bool(params[1].value)

        core.check.shapes(params[0].value)

        return


class Geometry(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Geometry"
        self.description = "Check PST and/or FBOUND geometry"
        self.canRunInBackground = False

    def getParameterInfo(self):
        fields = arcpy.Parameter(
            displayName="Shapefiles",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        fields.filter.list = ["PST", "FBOUND"]

        params = [fields]

        return params

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True

        _fields = params[0].valueAsText
        shapes = _fields.split(";")

        for _shape in shapes:
            if _shape == "PST":
                core.check.pst_geometry()
            elif _shape == "FBOUND":
                core.check.fbound_geometry()
            else:
                pass

        return


class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Check ROADS for intersections. By deafult the script checks the old ROADS in InputData"
        self.canRunInBackground = False

    def getParameterInfo(self):
        roads = arcpy.Parameter(
            displayName="Check new ROADS",
            name="roads",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        roads.value = "false"

        params = [roads]
        return params

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True
        new_roads = bool(params[0].value)

        if new_roads:
            roads = 'new'
        else:
            roads = 'old'

        core.check.roads(roads)

        return


class Dbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "DBOUND"
        self.description = "Check DBOUND for missing values"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.check.dbound()

        return


class Bld(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "BLD"
        self.description = "Check BLD for missing values"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.check.bld()

        return
