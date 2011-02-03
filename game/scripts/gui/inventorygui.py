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

from fife.extensions.pychan.tools import callbackWithArguments as cbwa
from fife.extensions import pychan
from fife.extensions.pychan.attrs import UnicodeAttr

from scripts.gui import drag_drop_data as data_drag
from scripts.objects.base import Container
from scripts.gui.containergui_base import ContainerGUIBase
from scripts.objects.action import ACTIONS

class EquipmentSlot(pychan.VBox):
    ATTRIBUTES = pychan.VBox.ATTRIBUTES + [UnicodeAttr('label_text')]
    
    def _setLabelText(self, text):
        label = self.findChild()
        label.text = unicode(text)
        label.resizeToContent()
        self.margins = (
            int((self.width - label.width) / 2.0),
            int((self.height - label.height) / 2.0)
        )
    
    def _getLabelText(self):
        label = self.findChild()
        return label.text
    
    label_text = property(fget=_getLabelText, fset=_setLabelText)
    
    def __init__(self, label_text=u'equipment', min_size=(50, 50),
                 max_size=(50, 50), margins=None,
                 background_image="gui/inv_images/inv_background.png",
                 **kwargs):
        pychan.VBox.__init__(self, min_size=min_size, max_size=max_size,
                             **kwargs)
        self.background_image = background_image
        label = pychan.Label(text=unicode(label_text))
        self.addChild(label)
        self.label_text = label_text
        self.adaptLayout()
        if self.parent is not None:
            self.beforeShow()


class InventoryGrid(pychan.VBox):
    ATTRIBUTES = pychan.VBox.ATTRIBUTES + [pychan.attrs.PointAttr('grid_size')]
    
    def _setNColumns(self, n_columns):
        n_rows = self.grid_size[1]
        self.grid_size = (n_columns, n_rows)
    
    def _getNColumns(self):
        n_columns = self.grid_size[0]
        return n_columns
    n_columns = property(fget=_getNColumns, fset=_setNColumns)
    
    def _setNRows(self, n_rows):
        n_columns = self.grid_size[0]
        self.grid_size = (n_columns, n_rows)
    
    def _getNRows(self):
        n_rows = self.grid_size[1]
        return n_rows
    n_rows = property(fget=_getNRows, fset=_getNColumns)
    
    def _setGridSize(self, grid_size):
        n_columns, n_rows = grid_size
        self.removeAllChildren()
        for row_n in range(n_rows):
            row_size = (n_columns * 50, 50)
            row = pychan.HBox(min_size=row_size, max_size=row_size,
                              padding=self.padding)
            row.border_size = 1
            row.opaque = 0
            for column_n in range(n_columns):
                slot = pychan.Icon(min_size=(50, 50), max_size=(50, 50))
                slot.border_size = 1
                row.addChild(slot)
            self.addChild(row)
        self.min_size = ((n_columns * 50) + 2, (n_rows * 50) + 2)
        self.max_size = self.min_size
    
    def _getGridSize(self):
        n_rows = len(self.children)
        n_columns = len(self.children[0].children)
        return (n_rows, n_columns)
    grid_size = property(fget=_getGridSize, fset=_setGridSize)
    
    def __init__(self, grid_size=(2, 2), padding=0, **kwargs):
        pychan.VBox.__init__(self, padding=padding, **kwargs)
        self.opaque = 0
        self.grid_size = grid_size
        self.border_size = 1


class InventoryGUI(ContainerGUIBase):
    def __init__(self, controller, inventory, callbacks):
        super(InventoryGUI, self).__init__(controller, "gui/inventory.xml")
        self.engine = controller.engine
        self.inventory_shown = False
        render_backend = self.engine.getRenderBackend()
        screen_mode = render_backend.getCurrentScreenMode()
        screen_width, screen_height = (screen_mode.getWidth(),
                                       screen_mode.getHeight())
        widget_width, widget_height = self.gui.size
        self.gui.position = ((screen_width - widget_width) / 2,
                             (screen_height - widget_height) / 2)
    
    def toggleInventory(self, toggleImage=True):
        """Pause the game and enter the inventory screen, or close the
           inventory screen and resume the game.
           @type toggleImage: bool
           @param toggleImage:
               Call toggleInventoryCallback if True. Toggling via a
               keypress requires that we toggle the Hud inventory image
               explicitly. Clicking on the Hud inventory button toggles the
               image implicitly, so we don't change it.
           @return: None"""
        if not self.inventory_shown:
            self.showInventory()
            self.inventory_shown = True
        else:
            self.closeInventory()
            self.inventory_shown = False
    
    def showInventory(self):
        self.gui.show()
    
    def closeInventory(self):
        self.gui.hide()


class _InventoryGUI(ContainerGUIBase):
    """Inventory GUI class"""
    def __init__(self, controller, inventory, callbacks):
        """Initialise the instance.
           @param controller: Current Controller
           @type controller: Class derived from ControllerBase
           @type inventory: Inventory
           @param inventory: An inventory object to be displayed and manipulated
           @type callbacks: dict
           @param callbacks: a dict of callbacks
               refreshReadyImages:
                   Function that will make the ready slots on the HUD
                   reflect those within the inventory
               toggleInventoryButton:
                   Function that will toggle the state of the inventory button
           @return: None"""
        super(InventoryGUI, self).__init__(controller, "gui/inventory.xml")
        self.engine = controller.engine
        self.readyCallback = callbacks['refreshReadyImages']
        self.toggleInventoryButtonCallback = callbacks['toggleInventoryButton']
        self.original_cursor_id = self.engine.getCursor().getId()

        self.inventory_shown = False
        events_to_map = {}
        self.inventory_storage = inventory
        
        # Buttons of inventory arranged by slots

        self.slot_buttons = {'head': ('Head',), 'chest': ('Body',),
                             'left_arm': ('LeftHand',),
                             'right_arm': ('RightHand',),
                             'hips' : ('Belt',), 'left_leg': ('LeftFoot',),
                             'right_leg': ('RightFoot',),
                             'left_hand': ('LeftHeld',),
                             'right_hand': ('RightHeld',),
                             'backpack': ('A1', 'A2', 'A3', 'A4', 'A5',
                                          'B1', 'B2', 'B3', 'B4', 'B5',
                                          'C1', 'C2', 'C3', 'C4', 'C5',
                                          'D1', 'D2', 'D3', 'D4', 'D5'),
                             'ready': ('Ready1', 'Ready2', 'Ready3', 'Ready4')
        }
        # the images that should be used for the buttons when they are "empty"
        self.slot_empty_images = {'head':'gui/inv_images/inv_head.png',
                                  'chest':'gui/inv_images/inv_torso.png',
                                  'left_arm':'gui/inv_images/inv_lhand.png',
                                  'right_arm':'gui/inv_images/inv_rhand.png',
                                  'hips':'gui/inv_images/inv_belt.png',
                                  'left_leg':'gui/inv_images/inv_lfoot.png',
                                  'right_leg':'gui/inv_images/inv_rfoot.png',
                                  'left_hand':'gui/inv_images/inv_litem.png',
                                  'right_hand':'gui/inv_images/inv_ritem.png',
                                  'backpack':'gui/inv_images/inv_backpack.png',
                                  'ready':'gui/inv_images/inv_belt_pouches.png',
                                  }
        self.updateInventoryButtons()

        for slot in self.slot_buttons:
            for _, button in enumerate(self.slot_buttons[slot]):
                events_to_map[button] = cbwa(self.dragDrop, button)
                events_to_map[button + "/mouseReleased"] = \
                                                self.showContextMenu
        events_to_map['close_button'] = self.closeInventoryAndToggle
        self.gui.mapEvents(events_to_map)
        # TODO: Why the commented out code?
        # self.resetMouseCursor()

    def updateImages(self):
        self.updateInventoryButtons()
    
    def updateInventoryButtons (self):
        for slot in self.slot_buttons:
            for index, button in enumerate(self.slot_buttons[slot]):
                widget = self.gui.findChild(name=button)
                widget.slot = slot
                widget.index = index
                widget.item = self.inventory_storage.getItemsInSlot(widget.slot,
                                                                   widget.index)
                self.updateImage(widget)
                
    def updateImage(self, button):
        if (button.item == None):
            image = self.slot_empty_images[button.slot]
        else:
            image = button.item.getInventoryThumbnail()
        button.up_image = image
        button.down_image = image
        button.hover_image = image

    def closeInventory(self):
        """Close the inventory.
           @return: None"""
        self.gui.hide()

    def closeInventoryAndToggle(self):
        """Close the inventory screen.
           @return: None"""
        self.closeInventory()
        self.toggleInventoryButtonCallback()
        self.inventory_shown = False

    def toggleInventory(self, toggleImage=True):
        """Pause the game and enter the inventory screen, or close the
           inventory screen and resume the game.
           @type toggleImage: bool
           @param toggleImage:
               Call toggleInventoryCallback if True. Toggling via a
               keypress requires that we toggle the Hud inventory image
               explicitly. Clicking on the Hud inventory button toggles the
               image implicitly, so we don't change it.
           @return: None"""
        if not self.inventory_shown:
            self.showInventory()
            self.inventory_shown = True
        else:
            self.closeInventory()
            self.inventory_shown = False

        if toggleImage:
            self.toggleInventoryButtonCallback()

    def showInventory(self):
        """Show the inventory.
           @return: None"""
        self.updateInventoryButtons()
        self.gui.show()                
                
    def dragObject(self, obj):
        """Drag the selected object.
           @type obj: string
           @param obj: The name of the object within
                       the dictionary 'self.buttons'
           @return: None"""
        # get the widget from the inventory with the name obj
        drag_widget = self.gui.findChild(name = obj)
        drag_item = drag_widget.item
        # only drag if the widget is not empty
        if (drag_item != None):
            # get the item that the widget is 'storing'
            data_drag.dragged_item = drag_widget.item
            # get the up and down images of the widget
            up_image = drag_widget.up_image
            down_image = drag_widget.down_image
            # set the mouse cursor to be the widget's image
            self.controller.setMouseCursor(up_image.source,down_image.source)
            data_drag.dragged_image = up_image.source
            data_drag.dragging = True
            data_drag.dragged_widget = drag_widget
            data_drag.source_container = self.inventory_storage
            
            self.inventory_storage.takeItem(drag_widget.item)
            # after dragging the 'item', set the widgets' images
            # so that it has it's default 'empty' images
            drag_widget.item = None
            self.updateImage(drag_widget)
            
            
    def dropObject(self, obj):
        """Drops the object being dropped
           @type obj: string
           @param obj: The name of the object within
                       the dictionary 'self.buttons' 
           @return: None"""
        drop_widget = self.gui.findChild(name = obj)
        drop_slot, drop_index = drop_widget.slot, drop_widget.index
        replace_item = None
        try :
            if data_drag.dragging:
                inventory = self.inventory_storage
                drag_item = data_drag.dragged_item
                #this will get the replacement item and data for drag_drop if
                ## there is an item All ready occupying the slot
                if not inventory.isSlotEmpty(drop_slot, drop_index):
                    #get the item and then remove it from the inventory
                    replace_item = inventory.getItemsInSlot \
                                                (drop_slot, drop_index)
                    self.dragObject(obj)
                self.inventory_storage.moveItemToSlot(drag_item,
                                                      drop_slot,
                                                      drop_index)
                    
            if drop_widget.slot == 'ready':
                self.readyCallback()
            
            if replace_item == None:
                self.controller.resetMouseCursor()
                data_drag.dragging = False
        except Container.TooBig :
            print("%s too big to fit into %s" % (data_drag.dragged_item,
                                                 drop_widget.slot))
        except (Container.SlotBusy, Container.ItemSelf):
            pass
        self.updateInventoryButtons()
              
    def createMenuItems(self, item, actions):
        """Creates context menu items for the InventoryGUI"""
        menu_actions = super(InventoryGUI, self).createMenuItems(item, actions)
        param_dict = {}
        param_dict["controller"] = self.controller
        param_dict["commands"] = {}
        param_dict["item"] = item
        param_dict["container_gui"] = self
        menu_actions.append(["Drop",
                             "Drop", 
                             self.executeMenuItem, 
                             ACTIONS["DropFromInventory"](**param_dict)])        
        return menu_actions
    
    def getImage(self, name):
        """Return a current image from the inventory
           @type name: string
           @param name: name of image to get
           @return: None"""
        return self.gui.findChild(name = name)
