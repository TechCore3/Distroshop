import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gdk

class DistroDetailsView(Adw.Bin):
    def __init__(self, window, distro):
        super().__init__()
        self.window = window
        self.distro = distro
        
        # Main Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        # Header Bar
        header = Adw.HeaderBar()
        main_box.append(header)
        
        # Main Scroll
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        main_box.append(scrolled)
        
        # Constraint Layout (clamp) to keep it readable
        clamp = Adw.Clamp()
        clamp.set_maximum_size(800)
        scrolled.set_child(clamp)
        
        # Content Box
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(40)
        box.set_margin_bottom(40)
        box.set_margin_start(20)
        box.set_margin_end(20)
        clamp.set_child(box)

        from core.image_cache import ImageLoader
        
        # Header: Icon + Title + Badges
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        box.append(header_box)
        
        self.icon_widget = Gtk.Image()
        self.icon_widget.set_pixel_size(96)
        header_box.append(self.icon_widget)
        
        # 1. Try Remote URL FIRST
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
                 self.icon_widget.set_from_icon_name("computer-symbolic")
        
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        title_box.set_valign(Gtk.Align.CENTER)
        header_box.append(title_box)
        
        title_lbl = Gtk.Label(label=distro.name)
        title_lbl.add_css_class("title-1")
        title_lbl.set_halign(Gtk.Align.START)
        title_box.append(title_lbl)
        
        tags_box = Gtk.Box(spacing=6)
        title_box.append(tags_box)
        
        for tag in distro.tags:
            lbl = Gtk.Label(label=tag)
            lbl.add_css_class("pill") # Adwaita generic pill if available or custom
            # Fallback to frame if no pill class
            tags_box.append(lbl)

        # Description
        desc_lbl = Gtk.Label(label=distro.description)
        desc_lbl.set_wrap(True)
        desc_lbl.set_halign(Gtk.Align.START)
        desc_lbl.add_css_class("body")
        box.append(desc_lbl)
        
        # Screenshots Carousel
        if distro.screenshot_urls:
             carousel = Adw.Carousel()
             carousel.set_spacing(10)
             carousel.set_vexpand(False)
             carousel.set_size_request(-1, 400) # Large height for screenshots
             carousel.set_allow_mouse_drag(True)
             box.append(carousel)
             
             for url in distro.screenshot_urls:
                 # Use Gtk.Picture for better aspect ratio handling in GTK4
                 img = Gtk.Picture()
                 img.set_can_shrink(True)
                 # ContentFit might not be available in older GTK4, but Picture scale naturally
                 try:
                     img.set_content_fit(Gtk.ContentFit.CONTAIN)
                 except:
                     pass
                 img.set_margin_start(10)
                 img.set_margin_end(10)
                 img.add_css_class("card")
                 
                 carousel.append(img)
                 ImageLoader.get_default().load_image(url, lambda u, t, i=img: i.set_paintable(t))
             
             # Indicators
             dots = Adw.CarouselIndicatorDots()
             dots.set_carousel(carousel)
             box.append(dots)

        # Action Buttons
        actions_box = Gtk.Box(spacing=10)
        actions_box.set_halign(Gtk.Align.CENTER)
        box.append(actions_box)
        
        # Website Button
        demo_btn = Gtk.Button(label="Website")
        demo_btn.add_css_class("suggested-action")
        demo_btn.add_css_class("pill")
        demo_btn.connect("clicked", self.on_demo_clicked)
        actions_box.append(demo_btn)

        # Download Button
        self.dl_btn = Gtk.Button(label="Download ISO")
        self.dl_btn.connect("clicked", self.on_download_clicked)
        actions_box.append(self.dl_btn)
        
        # Cancel Button (Hidden initially)
        self.cancel_btn = Gtk.Button(label="Cancel")
        self.cancel_btn.set_visible(False)
        self.cancel_btn.connect("clicked", self.on_cancel_clicked)
        actions_box.append(self.cancel_btn)
        
        # Etch to Disk Button
        self.etch_btn = Gtk.Button(label="Etch to Disk")
        self.etch_btn.connect("clicked", self.on_etch_clicked)
        actions_box.append(self.etch_btn)
        
        # Progress Bar (Hidden by default)
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_visible(False)
        self.pbar.set_show_text(True)
        box.append(self.pbar)
        
        # Downloader
        from core.downloader import DownloadManager
        self.downloader = DownloadManager()
        self.downloader.connect("progress", self.on_download_progress)
        self.downloader.connect("completed", self.on_download_completed)
        self.downloader.connect("error", self.on_download_error)
        
    def _on_image_loaded(self, url, texture):
        if url == self.distro.logo_url:
             self.icon_widget.set_from_paintable(texture)
    
    def on_demo_clicked(self, btn):
        print(f"Opening website for {self.distro.name}")
        # Launch default browser
        if self.distro.website:
             Gtk.show_uri(self.window, self.distro.website, Gdk.CURRENT_TIME)
        else:
            dialog = Adw.MessageDialog(
                heading="No Website Available",
                body="This distro does not have a website link.",
            )
            dialog.add_response("close", "Close")
            dialog.set_transient_for(self.window)
            dialog.present()
        
    def on_etch_clicked(self, btn):
        import os
        import glob
        from ui.usb_dialog import UsbDialog
        
        dl_dir = os.path.expanduser("~/Downloads/DistroExplorer")
        target_iso = None
        
        # 1. Check exact match (Our Downloader)
        exact_path = os.path.join(dl_dir, f"{self.distro.id}.iso")
        if os.path.exists(exact_path):
            target_iso = exact_path
        else:
            # 2. Fuzzy Search in Downloads folder(s)
            # Check ~/Downloads/DistroExplorer and ~/Downloads
            candidates = []
            keywords = self.distro.id.split('-') # e.g. "pop-os" -> "pop", "os"
            # Or use name parts. "Ubuntu"
            name_key = self.distro.name.split(' ')[0].lower() # "ubuntu"
            
            search_dirs = [dl_dir, os.path.expanduser("~/Downloads")]
            
            for d in search_dirs:
                if not os.path.exists(d): continue
                # Search for any iso containing the name key
                # This matches "ubuntu-24.04.iso" for "ubuntu"
                matches = glob.glob(os.path.join(d, f"*{name_key}*.iso"))
                if matches:
                    # Pick the most recent?
                    matches.sort(key=os.path.getmtime, reverse=True)
                    candidates.extend(matches)
            
            if candidates:
                target_iso = candidates[0]

        if not target_iso:
            dialog = Adw.MessageDialog(
                heading="ISO Not Found",
                body=f"Could not find an ISO for {self.distro.name} in Downloads.\n\nPlease download it first.",
            )
            dialog.add_response("ok", "OK")
            dialog.set_transient_for(self.window)
            dialog.present()
            return

        dialog = UsbDialog(self.window, target_iso)
        dialog.present()

        
    def on_download_clicked(self, btn):
        print(f"Downloading {self.distro.name}")
        url = self.distro.download_url
        if not url:
            dialog = Adw.MessageDialog(
                 heading="Direct Download Unavailable",
                 body=f"For {self.distro.name}, please download directly from their official website."
            )
            dialog.add_response("cancel", "Cancel")
            dialog.add_response("open", "Open Website")
            dialog.set_transient_for(self.window)
            dialog.connect("response", self.on_no_url_response)
            dialog.present()
            return
            
        filename = f"{self.distro.id}.iso"
        
        self.dl_btn.set_visible(False)
        self.cancel_btn.set_visible(True)
        
        self.pbar.set_visible(True)
        self.pbar.set_fraction(0)
        self.pbar.set_text("Starting download...")
        
        self.downloader.download_iso(url, filename)

    def on_no_url_response(self, dialog, response):
        if response == "open" and self.distro.website:
             Gtk.show_uri(self.window, self.distro.website, Gdk.CURRENT_TIME)
        dialog.close()
        
    def on_cancel_clicked(self, btn):
        self.downloader.cancel()
        self.cancel_btn.set_sensitive(False)
        self.pbar.set_text("Cancelling...")

    def on_download_progress(self, manager, progress):
        self.pbar.set_fraction(progress)
        self.pbar.set_text(f"{int(progress * 100)}%")

    def on_download_completed(self, manager, path):
        self.pbar.set_text("Download Complete!")
        self.pbar.set_fraction(1.0)
        
        self.dl_btn.set_visible(True)
        self.dl_btn.set_sensitive(True)
        self.cancel_btn.set_visible(False)
        self.cancel_btn.set_sensitive(True)
        
        print(f"File saved to {path}")
        
    def on_download_error(self, manager, error_msg):
        self.pbar.set_text(f"Error: {error_msg}")
        
        self.dl_btn.set_visible(True)
        self.dl_btn.set_sensitive(True)
        self.cancel_btn.set_visible(False)
        self.cancel_btn.set_sensitive(True)
