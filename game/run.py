#!/usr/bin/env python2

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import imp
import sys

#Check if config.py exists. Get 'fife_path' from config
try:
	import config
	sys.path.append(config.fife_path)
except:
	pass

try:
	from fife import fife
	print "Using the FIFE python module found here: ", \
		os.path.dirname(fife.__file__)
except ImportError:
	print "====================================================================== \n\
FIFE was not found in path. \n\
Try installing FIFE or creating config.py in the PARPG root directory, \n\
with a variable pointing to the 'python' subdirectory \n\
fife_path='<path_to_your_FIFE>' \n\
Example: fife_path='../fife/engine/python/' \n\
======================================================================"

from scripts.parpg import PARPGApplication
from scripts.common.utils import loadSettings

from scripts.common import utils

# add paths to the swig extensions
utils.addPaths ('../../engine/swigwrappers/python', '../../engine/extensions')
utils.addPaths ('./lib', './lib/extensions')


"""This folder holds the main meta-data for PARPG. This file should be
   minimal, since folding code into the controller with MVC is usually bad
   All game and logic and data is held held and referenced in 
   /scripts/engine.py. All fife stuff goes in /scripts/world.py"""

def main_is_frozen():
    """returns True when running the exe, 
    and False when running from a script. """
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
    """returns the directory name of the script 
    or the directory name of the exe"""
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])


def main():
    """Application code starts from here"""
    if not main_is_frozen():
        version = loadSettings().get("PARPG", "SettingsVersion")
        dist_version = loadSettings("./settings-dist.xml").get("PARPG", "SettingsVersion")
        if (version != dist_version):
            print "Newer settings-dist.xml found, renaming settings.xml to settings-old.xml"
            shutil.copyfile('./settings.xml', './settings-old.xml')
            shutil.copyfile('./settings-dist.xml', './settings.xml')
    app = PARPGApplication(loadSettings())
    app.run()

if __name__ == '__main__':
    if loadSettings().get("FIFE", "UsePsyco"):
        # Import Psyco if available
        try:
            import psyco
            psyco.full()
            print "Psyco acceleration in use"
        except ImportError:
            print "Psyco acceleration not used"
    else:
        print "Psyco acceleration not used"
    main()

