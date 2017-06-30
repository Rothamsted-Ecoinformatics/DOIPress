'''
Created on 26 Jun 2017

@author: ostlerr
'''
import sys
import cx_Freeze
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [cx_Freeze.Executable("doipress.py", base=base)]

addtional_mods = ['numpy.core._methods', 'numpy.lib.format']

packages = ["idna", "numpy",]
options = {
    'build_exe': {

        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            "config.ini",
            "rothamsted-favicon.ico",
         ],
        'includes': addtional_mods,
        'packages':packages,
    },

}

cx_Freeze.setup(
    name = "DOI Press",
    author = "Richard Ostler",
    options = options,
    version = "1.0",
    description = 'Simple tool for generating and logging a random string DOI',
    executables = executables
)