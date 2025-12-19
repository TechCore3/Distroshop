import os
import threading
import hashlib
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import GLib, GObject, Gdk, Gtk

class ImageLoader(GObject.Object):
    __gsignals__ = {
        'image-loaded': (GObject.SignalFlags.RUN_LAST, None, (str, Gdk.Texture)), # url, texture
    }

    _instance = None
    
    @classmethod
    def get_default(cls):
        if not cls._instance:
            cls._instance = ImageLoader()
        return cls._instance

    def __init__(self):
        super().__init__()
        # Using GLib to get standard XDG cache directory
        cache_base = GLib.get_user_cache_dir()
        self.cache_dir = os.path.join(cache_base, "distroexplorer", "assets_v2")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.memory_cache = {} # url -> texture

    def load_image(self, url, callback=None):
        """
        Request an image.
        """
        if not url:
            return None
            
        if url in self.memory_cache:
            if callback:
                callback(url, self.memory_cache[url])
            return self.memory_cache[url]

        # Check if local path (GTK version uses file://)
        if url.startswith("file://"):
            local_path = url[7:]
            if os.path.exists(local_path):
                try:
                    texture = Gdk.Texture.new_from_filename(local_path)
                    self.memory_cache[url] = texture
                    if callback:
                        callback(url, texture)
                    return texture
                except Exception as e:
                    print(f"Failed to load local image {local_path}: {e}")
            else:
                print(f"Local asset not found: {local_path}")
            
            # Fallback to placeholder for local failure too
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            placeholder_path = os.path.join(project_root, "assets", "placeholder.jpg")
            if os.path.exists(placeholder_path):
                 try:
                     texture = Gdk.Texture.new_from_filename(placeholder_path)
                     if callback:
                         callback(url, texture)
                 except:
                     pass
            return None

        # Check disk
        filename = hashlib.md5(url.encode('utf-8')).hexdigest() + ".png"
        filepath = os.path.join(self.cache_dir, filename)

        if os.path.exists(filepath):
            try:
                texture = Gdk.Texture.new_from_filename(filepath)
                self.memory_cache[url] = texture
                if callback:
                    callback(url, texture)
                return texture
            except Exception as e:
                print(f"Failed to load cached image {filepath}: {e}")
        
        # Download in background
        thread = threading.Thread(target=self._download_worker, args=(url, filepath, callback))
        thread.daemon = True
        thread.start()
        return None

    def _download_worker(self, url, filepath, callback):
        try:
            import urllib.request
            # Add User-Agent to avoid 403 Forbidden
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 DistroShop/1.0'
            }
            print(f"Downloading asset: {url}")
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            
            # Load back on main thread
            GLib.idle_add(self._on_download_complete, url, filepath, callback)
            
        except Exception as e:
            print(f"Error downloading image {url}: {e}")
            # Fallback to placeholder
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            placeholder_path = os.path.join(project_root, "assets", "placeholder.jpg")
            if os.path.exists(placeholder_path):
                 GLib.idle_add(self._on_download_complete, url, placeholder_path, callback)

    def _on_download_complete(self, url, filepath, callback):
        try:
            texture = Gdk.Texture.new_from_filename(filepath)
            self.memory_cache[url] = texture
            self.emit('image-loaded', url, texture)
            if callback:
                callback(url, texture)
        except Exception as e:
            print(f"Error loading downloaded image: {e}")
