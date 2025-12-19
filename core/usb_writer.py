import subprocess
import json
import threading
import gi
from gi.repository import GLib, GObject

class UsbWriter(GObject.Object):
    __gsignals__ = {
        'write-complete': (GObject.SignalFlags.RUN_LAST, None, (bool, str)), # success, message
        'write-output': (GObject.SignalFlags.RUN_LAST, None, (str,)), # stdout/stderr line
    }

    def list_usb_drives(self):
        """
        Returns a list of dicts: {'name': '/dev/sdb', 'size': '16G', 'model': 'SanDisk...'}
        """
        drives = []
        try:
            # lsblk -J -o NAME,SIZE,MODEL,TRAN,TYPE,HOTPLUG
            cmd = ["lsblk", "-J", "-o", "NAME,SIZE,MODEL,TRAN,TYPE,HOTPLUG,RM"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            for device in data.get("blockdevices", []):
                # Filter for removable drives (usb) or hotplug
                # Note: Logic can be tricky. Generally TRAN=usb is good check.
                is_usb = device.get("tran") == "usb"
                is_removable = device.get("rm") == True or device.get("hotplug") == True
                is_disk = device.get("type") == "disk"
                
                if is_disk and (is_usb or is_removable):
                    drives.append({
                        "device": f"/dev/{device['name']}",
                        "name": device.get("name"),
                        "size": device.get("size"),
                        "model": device.get("model", "Unknown Drive")
                    })
        except Exception as e:
            print(f"Error listing drives: {e}")
            
        return drives

    def write_iso(self, iso_path, target_device):
        """
        Writes ISO to target device using pkexec dd.
        """
        thread = threading.Thread(target=self._write_worker, args=(iso_path, target_device))
        thread.daemon = True
        thread.start()

    def _write_worker(self, iso_path, target_device):
        try:
            GLib.idle_add(self.emit, 'write-output', f"Starting write to {target_device}...")
            
            # Construct command
            # oflag=sync for safety
            cmd = [
                "pkexec", "dd", 
                f"if={iso_path}", 
                f"of={target_device}", 
                "bs=4M", 
                "status=progress", 
                "oflag=sync"
            ]
            
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                bufsize=1, 
                universal_newlines=True
            )
            
            # Read stderr (dd updates progress on stderr)
            for line in process.stderr:
                GLib.idle_add(self.emit, 'write-output', line.strip())
                
            process.wait()
            
            if process.returncode == 0:
                GLib.idle_add(self.emit, 'write-complete', True, "Write successful!")
            else:
                GLib.idle_add(self.emit, 'write-complete', False, f"Process failed with code {process.returncode}")

        except Exception as e:
            GLib.idle_add(self.emit, 'write-complete', False, str(e))
