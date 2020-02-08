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

    def getParameterInfo(self):
        return

    def updateParameters(self, params):
        return

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create[core.kt.mode].fbound()

        return


###############################################################################

class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Create New ROADS's"
        self.canRunInBackground = False

    def getParameterInfo(self):
        return

    def updateParameters(self, params):
        return

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create[core.kt.mode].roads()

        return


###############################################################################

class Diekdikisi(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FBOUND Claim"
        self.description = "Creare FBOUND claim"
        self.canRunInBackground = False

    def getParameterInfo(self):
        return

    def updateParameters(self, params):
        return

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create[core.kt.mode].fboundclaim()

        return


###############################################################################

class PreFbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "PRE_FBOUND"
        self.description = "Create PRE_FBOUND's"
        self.canRunInBackground = False

    def getParameterInfo(self):
        return

    def updateParameters(self, params):
        return

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create[core.kt.mode].pre_fbound()

        return
