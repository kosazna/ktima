from cust_win import *

locASTENOT = []
locASTIK = []
locASTOTA = []
locASTTOM = []
locBLD = []
locDBOUND = []
locEAS = []
locPST = []
locVST = []
locRBOUND = []
locROADS = []
locFBOUND = []


loc_fl = {"ASTENOT": locASTENOT,
          "ASTIK": locASTIK,
          "ASTOTA": locASTOTA,
          "ASTTOM": locASTTOM,
          "BLD": locBLD,
          "DBOUND": locDBOUND,
          "FBOUND": locFBOUND,
          "PST": locPST,
          "ROADS": locROADS,
          "EAS": locEAS,
          "VST": locVST,
          "RBOUND": locRBOUND}

for shape in loc_fl:
    print(shape)