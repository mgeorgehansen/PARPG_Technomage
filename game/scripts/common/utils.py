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

# Miscellaneous game functions

import os, sys, fnmatch

def addPaths (*paths):
    """Adds a list of paths to sys.path. Paths are expected to use forward
       slashes, for example '../../engine/extensions'. Slashes are converted
       to the OS-specific equivalent.
       @type paths: ???
       @param paths: Paths to files?
       @return: None"""
    for p in paths:
        if not p in sys.path:
            sys.path.append(os.path.sep.join(p.split('/')))

def parseBool(value):
    """Parses a string to get a boolean value"""
    if (value.isdigit()):
        return bool(int(value))
    elif (value.isalpha):
        return value.lower()[0] == "t"
    return False

def locateFiles(pattern, root=os.curdir):
    """Locate all files matching supplied filename pattern in and below
    supplied root directory."""
    for path, _, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

def loadSettings(settings_file = "./settings.xml"):
    from fife.extensions.fife_settings import Setting
    return Setting(app_name = "PARPG",
                   settings_file = settings_file, 
                   settings_gui_xml = "")  