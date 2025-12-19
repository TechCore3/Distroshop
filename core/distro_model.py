from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Distro:
    id: str
    name: str
    description: str
    logo_resource: str
    website: str
    download_url: str
    desktop_environment: str
    base: str  # e.g., Debian, Arch, Fedora
    tags: list[str]
    logo_url: str = ""
    screenshot_urls: list[str] = field(default_factory=list)
    
    # Placeholder for status
    is_installed: bool = False
    is_downloaded: bool = False
