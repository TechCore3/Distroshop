import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib, GObject
from core.usb_writer import UsbWriter

class UsbDialog(Adw.Window):
    def __init__(self, parent, iso_path):
        super().__init__(transient_for=parent)
        self.set_title("Etch to Disk")
        self.set_modal(True)
        self.set_default_size(500, 400)
        
        self.iso_path = iso_path
        self.writer = UsbWriter()
        self.writer.connect('write-output', self.on_output)
        self.writer.connect('write-complete', self.on_complete)

        # Content
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)
        self.set_content(content)
        
        # Header
        lbl = Gtk.Label(label=f"Writing ISO: {iso_path}")
        lbl.add_css_class("heading")
        content.append(lbl)
        
        warn = Gtk.Label(label="⚠️ WARNING: ALL DATA ON TARGET DRIVE WILL BE LOST!")
        warn.add_css_class("error")
        warn.add_css_class("title-3")
        content.append(warn)

        # Drive Selector (ComboBox)
        drive_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        content.append(drive_box)
        
        drive_lbl = Gtk.Label(label="Select Drive:")
        drive_box.append(drive_lbl)
        
        self.drive_model = Gtk.StringList()
        self.drive_combo = Gtk.DropDown(model=self.drive_model)
        self.drive_combo.set_hexpand(True)
        drive_box.append(self.drive_combo)
        
        refresh_btn = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_btn.connect("clicked", self.refresh_drives)
        drive_box.append(refresh_btn)
        
        self.drives = [] # List of dicts
        
        # Output Log
        log_scroll = Gtk.ScrolledWindow()
        log_scroll.set_vexpand(True)
        content.append(log_scroll)
        
        self.log_view = Gtk.TextView()
        self.log_view.set_editable(False)
        self.log_view.set_monospace(True)
        log_scroll.set_child(self.log_view)

        # Actions
        actions = Gtk.Box(spacing=10)
        actions.set_halign(Gtk.Align.END)
        content.append(actions)
        
        cancel = Gtk.Button(label="Cancel")
        cancel.connect("clicked", lambda x: self.close())
        actions.append(cancel)
        
        self.flash_btn = Gtk.Button(label="Flash!")
        self.flash_btn.add_css_class("destructive-action")
        self.flash_btn.connect("clicked", self.on_flash_clicked)
        actions.append(self.flash_btn)
        
        # Initial Refresh (Must be after UI init)
        self.refresh_drives(None)

    def refresh_drives(self, btn):
        self.drives = self.writer.list_usb_drives()
        # Rebuild model
        # StringList doesn't have clear(), so we make a new one
        new_model = Gtk.StringList()
        if not self.drives:
            new_model.append("No removable drives found")
            self.flash_btn.set_sensitive(False)
        else:
            for d in self.drives:
                label = f"{d['name']} ({d['size']} - {d['model']})"
                new_model.append(label)
            self.flash_btn.set_sensitive(True)
            
        self.drive_combo.set_model(new_model)

    def on_flash_clicked(self, btn):
        idx = self.drive_combo.get_selected()
        if idx == Gtk.INVALID_LIST_POSITION or not self.drives:
            return

        target = self.drives[idx]['device']
        
        # Confirm
        # Adw.MessageDialog here ideally, but standard dialog for speed
        # Actually since we are in a modal window, we just proceed or use a confirmation var.
        # Let's assume the big red warning and button is enough for MVP.
        
        self.flash_btn.set_sensitive(False)
        self.drive_combo.set_sensitive(False)
        self.log("Starting write process...")
        self.writer.write_iso(self.iso_path, target)

    def on_output(self, writer, line):
        self.log(line)

    def on_complete(self, writer, success, msg):
        self.log(f"\nDONE: {msg}")
        if success:
            self.flash_btn.set_label("Success")
        else:
            self.flash_btn.set_label("Failed")
            self.flash_btn.set_sensitive(True)
            self.drive_combo.set_sensitive(True)

    def log(self, text):
        buf = self.log_view.get_buffer()
        buf.insert(buf.get_end_iter(), text + "\n")
        # auto scroll?
