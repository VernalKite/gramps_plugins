import os, sys

here = os.path.dirname(os.path.abspath(__file__))
if here not in sys.path:
    sys.path.insert(0, here)

from gramps.gui.plug import tool
from collect import people_collector
from render import render

class StarDatArtOptions(tool.ToolOptions):
    pass

class StarDatArtTool(tool.Tool):

    def __init__(self, dbstate, user, options_class, name, callback=None):
        tool.Tool.__init__(self, dbstate, options_class, name)
        self._run()

    def _run(self):
        persons = people_collector(self.db)
        if not persons:
            self._msg("There is no people with birth dates.")
            return
        path = self._ask_path()
        if not path:
            return
        render(persons, path)
        self._msg("Image saved:\n%s" % path)

    def _ask_path(self):
        from gi.repository import Gtk
        dialog = Gtk.FileChooserDialog(
            title="Save image",
            parent=None,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons("_Cancel", Gtk.ResponseType.CANCEL,
                           "_Save", Gtk.ResponseType.OK)
        dialog.set_current_name("star_datart.png")
        dialog.set_do_overwrite_confirmation(True)

        f = Gtk.FileFilter()
        f.set_name("PNG image (*.png)")
        f.add_pattern("*.png")
        dialog.add_filter(f)

        path = None
        if dialog.run() == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            if not path.lower().endswith(".png"):
                path += ".png"
        dialog.destroy()
        return path

    def _msg(self, text):
        from gramps.gui.dialog import OkDialog
        OkDialog("Star Data Art", text)