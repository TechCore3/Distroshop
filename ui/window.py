import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

class DistroWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(1100, 750)
        self.set_title("DistroShop")
        self.set_icon_name("io.github.distroshop.DistroShop")

        # Main content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(content_box)


        # Main View Stack (Gtk.Stack for text-only tabs)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        # Top Tab Bar
        switcher = Gtk.StackSwitcher()
        switcher.set_stack(self.stack)
        switcher.set_halign(Gtk.Align.CENTER) # Center tabs
        switcher.set_margin_top(10)
        switcher.set_margin_bottom(10)
        content_box.append(switcher)
        
        content_box.append(self.stack)
        
        # Store Tab
        from ui.store_view import StoreView
        from ui.details_view import DistroDetailsView
        
        self.store_nav = Adw.NavigationView()
        self.store_view = StoreView(self)
        
        # Wrap StoreView in a NavigationPage
        store_page = Adw.NavigationPage(child=self.store_view, title="Store")
        self.store_nav.add(store_page)
        
        self.stack.add_titled(self.store_nav, "store", "Store")

        # Tools Tab (Snapshot)
        from ui.tools_view import ToolsView
        self.tools_view = ToolsView(self)
        self.stack.add_titled(self.tools_view, "tools", "Tools")

    def navigate_to_details(self, distro):
        from ui.details_view import DistroDetailsView
        details_view = DistroDetailsView(self, distro)
        # Wrap Details View in a NavigationPage
        details_page = Adw.NavigationPage(child=details_view, title=distro.name)
        self.store_nav.push(details_page)
