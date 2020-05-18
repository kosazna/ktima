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

    @staticmethod
    def getParameterInfo():
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

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        _fields = params[0].valueAsText
        shapes = _fields.split(";")

        for _shape in shapes:
            if _shape == "PST":
                core.fix.pst_geometry()
            elif _shape == "FBOUND":
                core.fix.fbound_geometry()
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

    @staticmethod
    def getParameterInfo():
        return

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        core.fix.roads()

        return


###############################################################################

class Fields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Fields"
        self.description = "Fix fields and filling missing values"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
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

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        _fields = params[0].valueAsText
        shapes = _fields.split(";")

        for _shape in shapes:
            if _shape == "ASTENOT":
                core.fields.astenot()
            elif _shape == "ASTTOM":
                core.fields.asttom()
            elif _shape == "PST":
                core.fields.pst()
            else:
                pass

        return
