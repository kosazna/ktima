# -*- coding: utf-8 -*-
import arcpy
import copy
from ktima.arc import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "ServerExport"
        self.alias = ""

        # List of tool classes associated with this toolbox
        if core.get_pass():
            if core.meleti == 'KT1-05':
                self.tools = [Merge, Queries, Info, Isolate, OtaExport, Identical, Export, ChangeMode]
            else:
                self.tools = [Merge, Queries, Info, Isolate, OtaExport, Identical, Export]
        else:
            self.tools = []


class Merge(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Merge Shapefiles"
        self.description = "ROADS merge is done in old ROADS by default"
        self.canRunInBackground = False

    def getParameterInfo(self):
        shape = arcpy.Parameter(
            displayName="Shapefiles",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        force = arcpy.Parameter(
            displayName="Force Merge",
            name="force merge",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        roads = arcpy.Parameter(
            displayName="Merge new ROADS",
            name="roads",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        if core.mxdName == core.mxdGeneralName or core.mxdName == core.mxdKtimaName:
            merging_list = copy.copy(core.lut.merging_list)

            shape.filter.list = merging_list

        force.value = "false"
        roads.value = "false"

        params = [shape, force, roads]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = False
        shapetype = params[0].valueAsText
        shapetypes = shapetype.split(";")

        force_merge = bool(params[1].value)
        new_roads = bool(params[2].value)

        if new_roads:
            roads = 'new'
            shapes = copy.copy(shapetypes)
        else:
            roads = 'old'
            shapes = copy.copy(shapetypes)
            try:
                shapes[shapes.index('ROADS')] = 'IROADS'
            except ValueError:
                pass

        if core.mxdName == core.mxdKtimaName:
            core.add_layer(shapes, lyr=True)
            core.geoprocessing.merge(shapetypes, force_merge, roads)
        else:
            core.pm('!! Merge is performed only in -- {} -- !!'.format(core.mxdKtimaName))

        return


class Queries(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Spatial Queries"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        shape = arcpy.Parameter(
            displayName="Query",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input")

        shape.filter.list = ["KAEK_in_DBOUND", "KAEK_in_ASTIK", "RD", "PR"]

        params = [shape]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True
        shapetype = params[0].valueAsText

        if shapetype == "KAEK_in_DBOUND":
            core.find.kaek_in_dbound()
        elif shapetype == "KAEK_in_ASTIK":
            core.find.kaek_in_astik()
        elif shapetype == "RD":
            core.find.rd()
        elif shapetype == "PR":
            core.find.pr()

        return


class Info(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Info ({})".format(core.meleti)
        self.description = "Show Shapefile status and problems of {}".format(core.meleti)
        self.canRunInBackground = False

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True

        core.status.show()


class Isolate(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Isolate"
        self.description = "Isolate features to the specific area of {}".format(core.meleti)
        self.canRunInBackground = False

    def getParameterInfo(self):
        shape = arcpy.Parameter(
            displayName="Shapefile",
            name="shapetype",
            datatype="Layer",
            parameterType="Required",
            direction="Input")

        params = [shape]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True
        shapetype = params[0].valueAsText

        core.general.isolate(shapetype)

        return


class OtaExport(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export / OTA"
        self.description = "Export Shapefiles to LocalData"
        self.canRunInBackground = False

    def getParameterInfo(self):
        shape = arcpy.Parameter(
            displayName="Shapefile",
            name="Shape",
            datatype="Layer",
            parameterType="Required",
            direction="Input")

        export = arcpy.Parameter(
            displayName="Export Shapefiles",
            name="export",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        database = arcpy.Parameter(
            displayName="Export MBD('s)",
            name="dtb",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        spatial = arcpy.Parameter(
            displayName="Spatial Selection    ( If UNCHECKED choose a field below )",
            name="shapetype",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        fields = arcpy.Parameter(
            displayName="Field-base Selection",
            name="field",
            datatype="String",
            parameterType="Optional",
            direction="Input")

        export.value = "true"
        database.value = "false"
        spatial.value = "true"
        fields.filter.list = []

        params = [shape, spatial, fields, export, database]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, params):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        if params[0].valueAsText:
            params[2].filter.list = core.list_fields(params[0].valueAsText, 'name')

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = False

        shapetype = params[0].valueAsText
        spatial = bool(params[1].valueAsText)
        field = params[2].valueAsText
        export = bool(params[3].valueAsText)
        dtbase = bool(params[4].valueAsText)

        core.general.export_per_ota(shapetype, spatial=spatial, field=field, export_shp=export, database=dtbase)

        return


class Identical(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Find Identical"
        self.description = "Identical"
        self.canRunInBackground = False

    def getParameterInfo(self):
        what = arcpy.Parameter(
            displayName="Shapefile",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        in_what = arcpy.Parameter(
            displayName="Spapefile to check against:",
            name="shapefile",
            datatype="Layer",
            parameterType="Required",
            direction="Input")

        export = arcpy.Parameter(
            displayName="Export Identical as Shapefile",
            name="dtb",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        fc_list = core.list_layers()
        export.value = "false"

        if fc_list:
            in_what.filter.list = fc_list
            what.filter.list = fc_list

        params = [what, in_what, export]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, params):
        new_list = core.list_layers()
        params[0].filter.list = new_list
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = False

        shapes = params[0].valueAsText
        what_to = shapes.split(";")

        in_what = params[1].valueAsText

        export = bool(params[2].valueAsText)

        core.find.find_identical(what_to, in_what, export)

        return


class ChangeMode(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! CHANGE MODE ({} All) !".format(core.meleti)
        self.description = "Changing check mode".format(core.meleti)
        self.canRunInBackground = False

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = True

        core.change_mode()


class Export(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Export to Server"
        self.description = "Export shapefiles to kthma_temp"
        self.canRunInBackground = False

    def getParameterInfo(self):
        what = arcpy.Parameter(
            displayName="Shapefile from {}".format('checks.gdb'),
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        fc_list = core.list_gdb(core.paths.gdb_check)

        what.filter.list = fc_list

        params = [what]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, params):
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        arcpy.env.addOutputsToMap = False

        shapes = params[0].valueAsText
        what_to = shapes.split(";")

        core.geoprocessing.export_to_server(what_to)

        return
