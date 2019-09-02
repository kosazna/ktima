# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
from ktima.paths import *


toolboxes = ["A) General",
             "B) Check",
             "C) Fix",
             "D) Create"]

files = [r'arc\__init__.py',
         r'arc\core.py',
         r'arc\data.py',
         r'arc\organize.py',
         r'arc\rename.py',
         r'win\auto.py',
         r'win\pass.py',
         r'__init__.py',
         r'cust_arc.py',
         r'cust_win.py',
         r'logger.py',
         r'paths.py',
         r'status.py',
         r'testing.py',
         r'uasm.py',
         r'win\update.py']


def update_from_server(folder):
    for tool in toolboxes:
        inpath = r"{}:\! aznavouridis.k\Diafora\logs\scripts\!Toolboxes\{}.py".format(folder, tool)
        outpath = r"C:\Program Files (x86)\ArcGIS\Desktop10.1\Tools\KT-Tools\{}.pyt".format(tool)
        c_copy(inpath, outpath)

    for name in files:
        inpath = r"{}:\! aznavouridis.k\Diafora\logs\scripts\{}".format(folder, name)
        outpath = r"C:\Python27\ArcGIS10.1\Lib\site-packages\ktima\{}".format(name)
        c_copy(inpath, outpath)


def main(_func, _action):
    def all_files(__action):
        for tool in toolboxes:
            inpath = r"C:\Python27\ArcGIS10.1\Lib\site-packages\ktima\!Toolboxes\{}.py".format(tool)
            outpath = r"{}:\Google Drive\Work\ktima\ktima 5\!Toolboxes\{}.py".format(gd[user], tool)
            if __action == 'push':
                c_copy(inpath, outpath)
            else:
                c_copy(outpath, inpath)

        for name in files:
            inpath = r"C:\Python27\ArcGIS10.1\Lib\site-packages\ktima\{}".format(name)
            outpath = r"{}:\Google Drive\Work\ktima\ktima 5\{}".format(gd[user], name)
            if __action == 'push':
                c_copy(inpath, outpath)
            else:
                c_copy(outpath, inpath)

    def tools():
        for tool in toolboxes:
            try:
                inpath = r"C:\Python27\ArcGIS10.1\Lib\site-packages\ktima\!Toolboxes\{}.py".format(tool)
                outpath = r"C:\Program Files (x86)\ArcGIS\Desktop10.1\Tools\KT-Tools\{}.pyt".format(tool)
                copyfile(inpath, outpath)
            except IOError:
                pass

    if _func == "all_files":
        all_files(_action)
    else:
        tools()


if __name__ == "__main__":
    func = str(sys.argv[1])
    action = str(sys.argv[2])
    main(func, action)
