# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                       2019                         #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import py_compile
from handler import *
from update import toolboxes


def compile_ktima():
    no_compile = ['testing', 'pass', 'mkbinary']
    src = cp([users, user, 'Desktop', 'compiled code'])

    for dirpath, dirnames, filenames in os.walk(src):
        for filename in filenames:
            basename = os.path.splitext(filename)[0]
            _src = os.path.join(dirpath, filename)
            if filename.endswith('.py') and basename not in toolboxes and basename not in no_compile:
                py_compile.compile(_src, doraise=True)
                os.remove(_src)
            elif filename.endswith('.py') and basename in toolboxes:
                _dst = os.path.join(dirpath, '{}.pyt'.format(basename))
                os.rename(_src, _dst)
            else:
                os.remove(_src)


if __name__ == "__main__":
    compile_ktima()
