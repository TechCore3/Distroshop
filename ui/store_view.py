import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from ui.widgets import DistroCard
from core.distro_data import get_all_distros

class StoreView(Adw.Bin):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.all_distros = get_all_distros()

        # Main layout box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)
        
        # Header Bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True) # Ensure buttons show
        # Add title widget or leave standard? 
        # Store view title is usually "Distro Explorer" or "Store".
        # Let's add a Title widget
        title = Adw.WindowTitle(title="DistroShop", subtitle="Store")
        header.set_title_widget(title)
        main_box.append(header)
        
        # Search Bar Area
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.set_margin_top(10)
        search_box.set_margin_bottom(10)
        search_box.set_margin_start(20)
        search_box.set_margin_end(20)
        main_box.append(search_box)
        
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search distributions...")
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self.on_search_changed)
        search_box.append(self.search_entry)

        # Tab Switcher (Segmented Button-like)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        view_switcher = Gtk.StackSwitcher()
        view_switcher.set_stack(self.stack)
        view_switcher.set_margin_bottom(10)
        main_box.append(view_switcher)
        
        main_box.append(self.stack)

        # Create Pages
        self.featured_page = self.create_featured_page()
        self.stack.add_titled(self.featured_page, "featured", "Featured")

        self.newbie_page = self.create_grid_page("Newbie")
        self.stack.add_titled(self.newbie_page, "newbie", "Newbie")
        
        self.customizable_page = self.create_grid_page("Customizable")
        self.stack.add_titled(self.customizable_page, "customizable", "Customizable")
        
        self.classics_page = self.create_grid_page("Classics")
        self.stack.add_titled(self.classics_page, "classics", "Classics")
        
        self.proprietary_page = self.create_grid_page("Proprietary")
        self.stack.add_titled(self.proprietary_page, "proprietary", "Proprietary")
        
        # Initial Load
        self.refresh_grids()

    def create_featured_page(self):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        scrolled.set_child(box)
        
        # Banner
        banner = Adw.StatusPage()
        banner.set_title("Welcome to DistroShop")
        banner.set_description("Find your perfect Linux distribution.")
        banner.set_icon_name("system-software-install")
        banner.set_vexpand(False)
        banner.set_size_request(-1, 200)
        box.append(banner)
        
        # Switching Helper
        switch_box = Gtk.Box(spacing=12)
        switch_box.set_halign(Gtk.Align.CENTER)
        box.append(switch_box)
        
        icon = Gtk.Image.new_from_icon_name("user-available-symbolic")
        switch_box.append(icon)
        
        lbl = Gtk.Label(label="Coming from Windows?")
        lbl.add_css_class("heading")
        switch_box.append(lbl)
        
        switch_btn = Gtk.Button(label="See Recommendations")
        switch_btn.add_css_class("suggested-action")
        switch_btn.add_css_class("pill")
        switch_btn.connect("clicked", lambda x: self.stack.set_visible_child_name("newbie"))
        switch_box.append(switch_btn)
        
        # Featured Section
        lbl = Gtk.Label(label="Featured Top Picks")
        lbl.add_css_class("title-2")
        lbl.set_halign(Gtk.Align.START)
        box.append(lbl)
        
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(10)
        flowbox.set_min_children_per_line(3)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox.set_row_spacing(20)
        flowbox.set_column_spacing(20)
        box.append(flowbox)
        scrolled._flowbox = flowbox # Hack to reuse populate logic if needed, but we might want custom logic
        
        # Navigation Buttons (Shortcuts)
        actions_box = Gtk.Box(spacing=10)
        actions_box.set_halign(Gtk.Align.CENTER)
        box.append(actions_box)
        
        def nav_btn(label, target):
            b = Gtk.Button(label=f"Browse {label}")
            b.add_css_class("pill")
            b.connect("clicked", lambda x: self.stack.set_visible_child_name(target))
            actions_box.append(b)
            
        nav_btn("Newbie Friendly", "newbie")
        nav_btn("Customizable", "customizable")
        nav_btn("Classics", "classics")

        return scrolled

    def create_grid_page(self, category):
        """Creates a scrolled window with a flowbox for the category."""
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(10) 
        flowbox.set_min_children_per_line(3)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox.set_margin_top(20)
        flowbox.set_margin_bottom(20)
        flowbox.set_margin_start(20)
        flowbox.set_margin_end(20)
        flowbox.set_row_spacing(20)
        flowbox.set_column_spacing(20)
        
        scrolled.set_child(flowbox)
        # Store reference to flowbox in the scrolled window for easy access
        scrolled._flowbox = flowbox 
        return scrolled

    def refresh_grids(self, query=""):
        lower_query = query.lower()
        
        # Helper to populate a specific grid
        def populate(page, tag_filter):
            flowbox = page._flowbox
            # Clear
            child = flowbox.get_first_child()
            while child:
                flowbox.remove(child)
                child = flowbox.get_first_child()
            
            # Fill
            for d in self.all_distros:
                # Filter by Query first
                if lower_query and (lower_query not in d.name.lower() and lower_query not in d.description.lower()):
                    continue
                
                # Filter by Tag
                # If tag_filter is "Featured", pick Popular ones
                if tag_filter == "Featured":
                     if "Popular" in d.tags or "Rolling" in d.tags: # Just a mix for featured
                         # Limit to a few?
                         pass
                     else:
                         continue
                elif tag_filter not in d.tags:
                    continue

                card = DistroCard(d, on_click_callback=self.on_card_clicked)
                flowbox.append(card)

        populate(self.featured_page, "Featured")
        populate(self.newbie_page, "Newbie")
        populate(self.customizable_page, "Customizable")
        populate(self.classics_page, "Classics")
        populate(self.proprietary_page, "Proprietary")

    def on_search_changed(self, entry):
        query = entry.get_text()
        self.refresh_grids(query)
        
    def on_card_clicked(self, distro):
        self.window.navigate_to_details(distro)
