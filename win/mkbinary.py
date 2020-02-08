# -*- coding: utf-8 -*-
# ---------------------------------------------------#
#        Ergaleia Xorikwn Elegxwn Shapefile          #
#                    2019 - 2020                     #
#             Aznavouridis Konstantinos              #
#                                                    #
#             aznavouridis.k@gmail.com               #
# ---------------------------------------------------#
import py_compile
from ktima.handler import *
from update import toolboxes


def compile_ktima():
    no_compile = ['testing', 'pass', 'mkbinary']
    src = cp([users, user, 'Desktop', 'compiled code'])

    for fullpath, filename, basename, ext in list_dir(src, match='.py'):
        if basename not in toolboxes and basename not in no_compile:
            py_compile.compile(fullpath, doraise=True)
            os.remove(fullpath)
        elif basename in toolboxes:
            relative = os.path.split(fullpath)[0]
            new_path = os.path.join(relative, '{}.pyt'.format(basename))
            os.rename(fullpath, new_path)
        else:
            os.remove(fullpath)


if __name__ == "__main__":
    compile_ktima()
