import gi
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from core.package_manager import PackageManager

class ToolsView(Adw.PreferencesPage):
    def __init__(self, window):
        super().__init__()
        self.window = window
        # PreferencesPage doesn't have set_title/description in the same way as StatusPage for the banner,
        # but it works well for list of items. We can add a banner if needed, but standard PrefsPage is fine.
        
        # Snapshot Group
        group = Adw.PreferencesGroup()
        group.set_title("System Snapshot")
        group.set_description("Capture a list of all installed packages on this system.")
        self.add(group)

        row = Adw.ActionRow()
        row.set_title("Create Package Snapshot")
        row.set_subtitle("Save to ~/package_snapshot.txt")
        group.add(row)

        btn = Gtk.Button(label="Snapshot")
        btn.set_valign(Gtk.Align.CENTER)
        btn.connect("clicked", self.on_snapshot_clicked)
        row.add_suffix(btn)
        
        # Status "Row" (using a group for status output for now, or a toast)
        # Using a ToastOverlay is better for status, but for MVP let's add a row with label.
        self.status_group = Adw.PreferencesGroup()
        self.status_group.set_title("Status")
        self.add(self.status_group)
        
        self.status_row = Adw.ActionRow()
        self.status_row.set_title("Ready")
        self.status_group.add(self.status_row)

    def on_snapshot_clicked(self, btn):
        pm = PackageManager()
        output_path = os.path.expanduser("~/package_snapshot.txt")
        success, msg = pm.snapshot_packages(output_path)
        
        self.status_row.set_title(msg)
        if success:
            self.status_row.add_css_class("success")
        else:
            self.status_row.add_css_class("error")
