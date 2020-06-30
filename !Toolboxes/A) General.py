# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import arcpy
import copy
from ktima.arc import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "General_Tasks"
        self.alias = ""

        # List of tool classes associated with this toolbox
        if core.get_pass():
            self.tools = [Merge, Queries, Info, Isolate, OtaExport,
                          Identical, ExportToServer, ChangeMode, MonthReport]
        else:
            self.tools = []


###############################################################################

class ChangeMode(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Change Mode !"
        self.description = "Changing check mode"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        mode = arcpy.Parameter(
            displayName="Mode",
            name="Mode",
            datatype="String",
            parameterType="Required",
            direction="Input")

        company = arcpy.Parameter(
            displayName="Company",
            name="company",
            datatype="String",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        otas = arcpy.Parameter(
            displayName="OTA",
            name="OTA",
            datatype="String",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        default = arcpy.Parameter(
            displayName="Set as Default Mode",
            name="default",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        mode.value = core.kt.mode
        mode.filter.list = ['ktima', 'standalone']

        if core.kt.mode == core.KTIMA_MODE:
            otas.filter.list = []
            company.filter.list = []
        else:
            otas.filter.list = core.info.mel_ota_list
            company.filter.list = core.info.comps

        default.value = "false"

        params = [mode, company, otas, default]

        return params

    @staticmethod
    def updateParameters(params):
        if params[0].valueAsText == 'standalone':
            otas_values = copy.copy(core.info.mel_ota_list)
            params[2].filter.list = otas_values
            params[1].filter.list = core.info.comps

            companies = params[1].valueAsText

            if companies:
                params[2].values = core.get_otas(companies.split(';'))
        else:
            params[2].filter.list = []
            params[1].filter.list = []

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True

        mode = params[0].valueAsText
        _otas = params[2].valueAsText
        default = bool(params[3].value)

        if _otas:
            otas = _otas.split(';')
        else:
            otas = core.info.ota_list

        if default:
            core.kt.set_default_mode(mode)

        core.check_ktima_version()
        core.kt.reset_mode(mode, core.strize(otas))


###############################################################################

class Info(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Info ({})".format(core.MELETI)
        self.description = "Show Shapefile status and problems of {}".format(
            core.MELETI)
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
        core.status[core.kt.mode].show()


###############################################################################

class OtaExport(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export / OTA"
        self.description = "Export Shapefiles to LocalData"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
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
            displayName="Spatial Selection (If UNCHECKED choose a field below)",
            name="shapetype",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        spatial_method = arcpy.Parameter(
            displayName="Spatial Method",
            name="spatial_method",
            datatype="String",
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
        spatial_method.value = 'location_within'
        spatial_method.filter.list = ['location_within', 'location_intersect',
                                      'intersect']

        params = [shape, spatial, spatial_method, fields, export, database]
        return params

    @staticmethod
    def updateParameters(params):
        if params[0].valueAsText:
            params[3].filter.list = core.list_fields(params[0].valueAsText,
                                                     'name')

        return params

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        shape = params[0].valueAsText
        spatial = bool(params[1].value)
        spatial_method = params[2].valueAsText
        field = params[3].valueAsText
        export = bool(params[4].value)
        dtbase = bool(params[5].value)

        core.check_ktima_version()
        core.general.export_per_ota(shape,
                                    spatial=spatial,
                                    spatial_method=spatial_method,
                                    field=field,
                                    export_shp=export,
                                    database=dtbase)

        return


###############################################################################

class ExportToServer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Export to Server"
        self.description = "Export shp_list to kthma_temp"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        geodatabase = arcpy.Parameter(
            displayName="Geodatabase",
            name="geodatabase",
            datatype="String",
            parameterType="Required",
            direction="Input")

        shapes = arcpy.Parameter(
            displayName="File GeoDatabase Files",
            name="shp_list",
            datatype="String",
            parameterType="Optional",
            direction="Input",
            multiValue=True)

        geodatabase.value = core.kt.mode
        geodatabase.filter.list = ['ktima', 'standalone']

        if core.kt.mode == core.KTIMA_MODE:
            _path = core.paths.gdb_ktima
        else:
            _path = core.paths.gdb_standalone

        shapes.filter.list = core.list_gdb(_path)

        params = [geodatabase, shapes]

        return params

    @staticmethod
    def updateParameters(params):
        if params[0].valueAsText == 'ktima':
            _path = core.paths.gdb_ktima
            params[1].filter.list = core.list_gdb(_path)
        else:
            _path = core.paths.gdb_standalone
            params[1].filter.list = core.list_gdb(_path)

        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        geodatabse = params[0].valueAsText
        _shapes = params[1].valueAsText

        shapes = _shapes.split(";")

        core.check_ktima_version()
        core.general.export_to_server(shapes, geodatabse)

        return


###############################################################################

class Identical(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Find Identical"
        self.description = "Identical"
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
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

    @staticmethod
    def updateParameters(params):
        new_list = core.list_layers()
        params[0].filter.list = new_list
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False

        shapes = params[0].valueAsText
        what_to = shapes.split(";")

        in_what = params[1].valueAsText

        export = bool(params[2].value)

        core.check_ktima_version()
        core.find.find_identical(what_to, in_what, export)

        return


###############################################################################

class Isolate(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Isolate"
        self.description = "Isolate features to the specific area of {}".format(
            core.MELETI)
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        shape = arcpy.Parameter(
            displayName="Shapefile",
            name="shapetype",
            datatype="Layer",
            parameterType="Required",
            direction="Input")

        params = [shape]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True
        shapetype = params[0].valueAsText

        core.check_ktima_version()
        core.general.isolate(shapetype)

        return


###############################################################################

class Merge(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Merge Shapefiles"
        self.description = "ROADS merge is done in old ROADS by default"
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

        force = arcpy.Parameter(
            displayName="Force Merge",
            name="force merge",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        missing = arcpy.Parameter(
            displayName="Ignore Missing",
            name="missing",
            datatype="Boolean",
            parameterType="Required",
            direction="Input")

        merging_list = copy.copy(core.info.merging_list)

        shape.filter.list = merging_list

        force.value = "false"
        missing.value = "false"

        params = [shape, force, missing]
        return params

    @staticmethod
    def updateParameters(params):

        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = False
        shapetype = params[0].valueAsText
        # otas_to_merge = params[4].valueAsText

        shapetypes = shapetype.split(";")

        force_merge = bool(params[1].value)
        _missing = bool(params[2].value)

        if _missing:
            missing = 'ignore'
        else:
            missing = 'raise'

        core.org.add_layer(shapetypes, lyr=True)

        core.check_ktima_version()
        core.geoprocessing.merge(shapetypes,
                                 force_merge,
                                 missing)

        return


###############################################################################

class Queries(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Spatial Queries"
        self.description = ""
        self.canRunInBackground = False

    @staticmethod
    def getParameterInfo():
        shape = arcpy.Parameter(
            displayName="Query",
            name="shapetype",
            datatype="String",
            parameterType="Required",
            direction="Input")

        shape.filter.list = ["KAEK_in_DBOUND", "KAEK_in_ASTIK", "RD", "PR"]

        params = [shape]
        return params

    @staticmethod
    def updateParameters(params):
        return

    @staticmethod
    def execute(params, messages):
        arcpy.env.addOutputsToMap = True
        shapetype = params[0].valueAsText

        core.check_ktima_version()

        if shapetype == "KAEK_in_DBOUND":
            core.find.kaek_in_dbound()
        elif shapetype == "KAEK_in_ASTIK":
            core.find.kaek_in_astik()
        elif shapetype == "RD":
            core.find.rd()
        elif shapetype == "PR":
            core.find.pr()

        return


class MonthReport(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "! Month Report"
        self.description = "Month Report"
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
        core.general.month_report()