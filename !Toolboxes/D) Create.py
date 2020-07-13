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
        self.label = "Create"
        self.alias = ""

        # List of tool classes associated with this toolbox
        if core.get_pass():
            self.tools = [Fbound, Roads, Diekdikisi, PreFbound]
        else:
            self.tools = []


###############################################################################

class Fbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FBOUND"
        self.description = "Create new FBOUND's"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        po = arcpy.Parameter(
            displayName="Which FOREST File",
            name="forest",
            datatype="String",
            parameterType="Required",
            direction="Input")

        po_files = core.file_path_dict(core.paths.input_po, match='.shp')
        po.filter.list = po_files.keys()

        params = [po]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        po_files = core.file_path_dict(core.paths.input_po, match='.shp')

        po = params[0].valueAsText
        po_file = po_files[po]

        core.check_ktima_version()
        core.create.fbound(po_file)

        return


###############################################################################

class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Create New ROADS's"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        st_ignore = arcpy.Parameter(
            displayName="Ignore Status",
            name="ignore status",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        st_ignore.value = "false"

        params = [st_ignore]

        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        ignore_status = bool(params[0].value)

        core.check_ktima_version()
        core.create.roads(ignore_status=ignore_status)

        return


###############################################################################

class Diekdikisi(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FBOUND Claim"
        self.description = "Creare FBOUND claim"
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
        core.create.fboundclaim()

        return


###############################################################################

class PreFbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "PRE_FBOUND"
        self.description = "Create PRE_FBOUND's"
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
        core.create.pre_fbound()

        return
