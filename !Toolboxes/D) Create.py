# -*- coding: utf-8 -*-
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


class Fbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FBOUND"
        self.description = "Create new FBOUND's"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create.fbound()

        return


class Roads(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ROADS"
        self.description = "Create New ROADS's"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create.roads()

        return


class Diekdikisi(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FBOUND Claim"
        self.description = "Creare FBOUND claim"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create.fboundclaim()

        return


class PreFbound(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "PRE_FBOUND"
        self.description = "Create PRE_FBOUND's"
        self.canRunInBackground = False

    def execute(self, parameters, messages):
        arcpy.env.addOutputsToMap = True

        core.create.pre_fbound()

        return
