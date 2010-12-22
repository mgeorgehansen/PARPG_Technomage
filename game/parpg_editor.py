#!/usr/bin/env python2

#   This file is part of PARPG.
#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

"""
This runs the editor in ..\tools\map_editor\run.py
"""

if __name__ == '__main__':
    parpg_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    parpg_dir = parpg_path.split('/')[-1]

    args = [sys.executable, './run.py']

    if len(sys.argv) > 1:
        map_path = sys.argv[1]

        args.append(os.path.join('..', parpg_dir, map_path))
        print args

    fife_editor_path = os.path.join(parpg_path, '..', 'tools', 'map_editor')
    os.chdir(fife_editor_path)
    os.execv(args[0], args)
