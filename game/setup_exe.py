from distutils.core import setup
import py2exe    

excludes = ['_scproxy', 'dummy.Process', 'guichan', 'objects.createObject']

setup(options = {"py2exe":{
                 "excludes": excludes}
                 },
      console = [{"script": "run.py", 
                  "dest_base": "Parpg",
                  "icon_resources": [(1, "gui/icons/window_icon.ico")]}])