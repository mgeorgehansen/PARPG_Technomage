#!/usr/bin/env python

#   This file is part of PARPG.

#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ["MapItem", ]

from composed import CarryableItem

class MapItem(CarryableItem):
    """Item that is lying on a map"""
    def __init__(self, ID, item_type, item, name = 'Item', text = 'An item',
                   gfx = 'item', **kwargs):
        CarryableItem.__init__(self, ID = ID, item_type = item_type, name = name, 
                               text = text, gfx = gfx, **kwargs)
        self.item = item