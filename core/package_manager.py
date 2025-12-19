import shutil
import subprocess
import os

class PackageManager:
    def __init__(self):
        self.manager = self._detect_manager()

    def _detect_manager(self):
        if shutil.which("dpkg"):
            return "dpkg"
        elif shutil.which("rpm"):
            return "rpm"
        elif shutil.which("pacman"):
            return "pacman"
        else:
            return "unknown"

    def snapshot_packages(self, output_file):
        """
        Dumps the list of installed packages to the output file.
        """
        try:
            if self.manager == "dpkg":
                # Debian/Ubuntu: dpkg --get-selections
                cmd = ["dpkg", "--get-selections"]
                with open(output_file, "w") as f:
                    subprocess.run(cmd, stdout=f, check=True)
            
            elif self.manager == "rpm":
                # Fedora/RHEL: rpm -qa
                cmd = ["rpm", "-qa"]
                with open(output_file, "w") as f:
                    subprocess.run(cmd, stdout=f, check=True)
            
            elif self.manager == "pacman":
                # Arch: pacman -Q
                cmd = ["pacman", "-Q"]
                with open(output_file, "w") as f:
                    subprocess.run(cmd, stdout=f, check=True)
            
            else:
                return False, "Unknown Package Manager"

            return True, f"Snapshot saved to {output_file} using {self.manager}"
            
        except subprocess.CalledProcessError as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
