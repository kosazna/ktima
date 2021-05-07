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
            fields.filter.list = ["PST", "FBOUND", "EAS"]
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

        core.check_ktima_version()

        for _shape in shapes:
            if _shape == "PST":
                core.fix.pst_geometry()
            elif _shape == "FBOUND":
                core.fix.fbound_geometry()
            elif _shape == "EAS":
                core.fix.eas_geometry()
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
        buffer_d = arcpy.Parameter(
            displayName="Buffer:",
            name="buffer",
            datatype="Double",
            parameterType="Required",
            direction="Input")

        st_ignore = arcpy.Parameter(
            displayName="Ignore Status",
            name="ignore status",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        i_ignore = arcpy.Parameter(
            displayName="Ignore Intersections",
            name="ignore intersections",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        buffer_d.value = core.ns.ek_bound_reduction
        st_ignore.value = "false"
        i_ignore.value = "false"

        params = [buffer_d, st_ignore, i_ignore]

        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        buffer_d = params[0].value
        ignore_status = bool(params[1].value)
        ignore_intersections = bool(params[2].value)

        core.check_ktima_version()
        core.fix.roads(buffer_dist=buffer_d, ignore_status=ignore_status,
                       ignore_intersections=ignore_intersections)

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

        fields.filter.list = ["ASTENOT", "ASTTOM", "PST", "FBOUND_DOC_ID"]

        params = [fields]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        _fields = str(params[0].valueAsText)

        shapes = _fields.split(";")

        core.pm(shapes)

        core.check_ktima_version()

        for _shape in shapes:
            if _shape == "ASTENOT":
                core.fields.astenot()
            elif _shape == "ASTTOM":
                core.fields.asttom()
            elif _shape == "PST":
                core.fields.pst()
            elif _shape == "FBOUND_DOC_ID":
                core.fields.fbound_docs()
            else:
                pass

        return
