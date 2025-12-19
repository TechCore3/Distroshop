import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject

class DistroCard(Gtk.Button):
    __gtype_name__ = 'DistroCard'

    def __init__(self, distro, on_click_callback=None):
        super().__init__()
        self.distro = distro
        self.on_click = on_click_callback
        
        self.add_css_class("card")
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)
        # Fixed size for grid consistency
        self.set_size_request(200, 250) 
        self.set_has_frame(False) # Flat look

        if self.on_click:
            self.connect("clicked", lambda x: self.on_click(self.distro))
            
        from core.image_cache import ImageLoader

        # Content
        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        inner_box.set_margin_top(12)
        inner_box.set_margin_bottom(12)
        inner_box.set_margin_start(12)
        inner_box.set_margin_end(12)
        self.set_child(inner_box)

        # Logo Image
        self.icon_widget = Gtk.Image()
        self.icon_widget.set_pixel_size(64)
        self.icon_widget.set_halign(Gtk.Align.CENTER)
        inner_box.append(self.icon_widget)
        
        # 1. Try Remote URL FIRST (as requested by user to use their links)
        if distro.logo_url:
            self.icon_widget.set_from_icon_name("computer-symbolic")
            ImageLoader.get_default().load_image(distro.logo_url, self._on_image_loaded)
        else:
            # 2. Try Local Resource
            icon_name = distro.logo_resource
            display = Gtk.Widget.get_display(self)
            theme = Gtk.IconTheme.get_for_display(display)
            
            if theme.has_icon(icon_name):
                 self.icon_widget.set_from_icon_name(icon_name)
            else:
                # 3. Fallback
                self.icon_widget.set_from_icon_name("computer-symbolic")

        # Name
        name_label = Gtk.Label(label=distro.name)
        name_label.add_css_class("title-3")
        name_label.set_halign(Gtk.Align.CENTER)
        inner_box.append(name_label)

        # DE Badge (simplified)
        de_label = Gtk.Label(label=distro.desktop_environment)
        de_label.add_css_class("dim-label")
        de_label.set_halign(Gtk.Align.CENTER)
        inner_box.append(de_label)
        
        # Description (Short)
        desc = Gtk.Label(label=distro.description)
        desc.set_wrap(True)
        desc.set_max_width_chars(20)
        desc.set_lines(3)
        desc.set_ellipsize(3) # Pango.EllipsizeMode.END
        inner_box.append(desc)

    def _on_image_loaded(self, url, texture):
        if url == self.distro.logo_url:
             self.icon_widget.set_from_paintable(texture)
