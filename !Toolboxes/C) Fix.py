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
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        if core.get_pass():
            self.tools = [Geometry, Roads, Fields]
        else:
            self.tools = []


###############################################################################

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

        if core.mxdName == core.mxdKtimaName:
            fields.filter.list = ["PST", "FBOUND"]
        else:
            fields.filter.list = ["PST"]

        params = [fields]
        return params

    def updateParameters(self, params):
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = False

        _fields = params[0].valueAsText
        shapes = _fields.split(";")

        for _shape in shapes:
            if _shape == "PST":
                core.fix[core.kt.mode].pst_geometry()
            elif _shape == "FBOUND":
                core.fix[core.kt.mode].fbound_geometry()
            else:
                pass

        return


###############################################################################

class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Fix roads so as not to intersect with nothing"
        self.canRunInBackground = False

    def getParameterInfo(self):
        return

    def updateParameters(self, params):
        return

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fix[core.kt.mode].roads()

        return


###############################################################################

class Fields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Fields"
        self.description = "Fix fields and filling missing values"
        self.canRunInBackground = False

    def getParameterInfo(self):
        fields = arcpy.Parameter(
            displayName="Shapefiles",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        fields.filter.list = ["ASTENOT", "ASTTOM", "PST"]

        params = [fields]
        return params

    def updateParameters(self, params):
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = False

        _fields = params[0].valueAsText
        shapes = _fields.split(";")

        for _shape in shapes:
            if _shape == "ASTENOT":
                core.fields[core.kt.mode].astenot()
            elif _shape == "ASTTOM":
                core.fields[core.kt.mode].asttom()
            elif _shape == "PST":
                core.fields[core.kt.mode].pst()
            else:
                pass

        return
