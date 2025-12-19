import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from ui.window import DistroWindow

class DistroExplorerApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id='io.github.distroshop.DistroShop',
                         flags=0,
                         **kwargs)

    def do_startup(self):
        Adw.Application.do_startup(self)
        # Fix: Using Adw.StyleManager in startup for best effect
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DistroWindow(application=self)
        win.present()

def main():
    app = DistroExplorerApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    main()
