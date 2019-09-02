# -*- coding: utf-8 -*-
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


class GeometryPst(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Geometry Shapefiles"
        self.description = "Fix geometry of all problematic shapefiles"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fix.pst_geometry()

        return


class GeometryFbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Geometry FBOUND"
        self.description = "Fix geometry of problematic FBOUND's"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fix.fbound_geometry()

        return


class Geometry(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Geometry"
        self.description = "Check PST and/or FBOUND geometry"
        self.canRunInBackground = False

    def getParameterInfo(self):
        fields = arcpy.Parameter(
            displayName="Shape",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        if core.mxdName == core.mxdGeneralName or core.mxdName == core.mxdKtimaName:
            fields.filter.list = ["PST", "FBOUND"]
        else:
            fields.filter.list = ["PST"]

        params = [fields]
        return params

    def execute(self, params, messages):
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


class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Fix roads so as not to intersect with nothing"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fix.roads()

        return


class PstFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Fields PST"
        self.description = ""
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fields.pst()

        return


class AsttomFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Fields ASTTOM"
        self.description = ""
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fields.asttom()

        return


class AstenotFields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Fields ASTENOT"
        self.description = ""
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = False

        core.fields.astenot()

        return


class Fields(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Fields"
        self.description = "Fix fields and filling missing values"
        self.canRunInBackground = False

    def getParameterInfo(self):
        fields = arcpy.Parameter(
            displayName="Shape",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        fields.filter.list = ["ASTENOT", "ASTTOM", "PST"]

        params = [fields]
        return params

    def execute(self, params, messages):
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
