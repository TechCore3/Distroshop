import threading
import urllib.request
import os
import gi
from gi.repository import GLib, GObject

class DownloadManager(GObject.Object):
    __gsignals__ = {
        'progress': (GObject.SignalFlags.RUN_LAST, None, (float,)), # progress 0.0 to 1.0
        'completed': (GObject.SignalFlags.RUN_LAST, None, (str,)), # file_path
        'error': (GObject.SignalFlags.RUN_LAST, None, (str,)) # error message
    }

    def __init__(self):
        super().__init__()
        # Use standard GLib path for Downloads
        downloads = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
        if not downloads:
            downloads = os.path.expanduser("~/Downloads")
        
        self.download_dir = os.path.join(downloads, "DistroExplorer")
        os.makedirs(self.download_dir, exist_ok=True)
        self._thread = None
        self._stop_event = threading.Event()

    def download_iso(self, url, filename):
        if self._thread and self._thread.is_alive():
            print("Download already in progress")
            return

        self._stop_event.clear()
        target_path = os.path.join(self.download_dir, filename)
        
        self._thread = threading.Thread(target=self._worker, args=(url, target_path))
        self._thread.daemon = True
        self._thread.start()

    def cancel(self):
        self._stop_event.set()

    def _worker(self, url, target_path):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 DistroShop/1.0'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                total_size = int(response.info().get('Content-Length', 0))
                downloaded_size = 0
                
                with open(target_path, 'wb') as f:
                    while True:
                        if self._stop_event.is_set():
                            GLib.idle_add(self.emit, 'error', "Download cancelled")
                            return
                        
                        chunk = response.read(8192)
                        if not chunk:
                            break
                            
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = downloaded_size / total_size
                            GLib.idle_add(self.emit, 'progress', progress)
            
            GLib.idle_add(self.emit, 'completed', target_path)

        except Exception as e:
            GLib.idle_add(self.emit, 'error', str(e))
