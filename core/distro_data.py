import os
from .distro_model import Distro

def get_asset(filename, remote_url):
    """
    Returns the local file:// path if filename exists in src/assets,
    otherwise returns the remote_url.
    """
    # Path relative to this file (src/core/distro_data.py)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_path = os.path.join(base_dir, "assets", filename)
    
    if os.path.exists(local_path):
        return f"file://{local_path}"
    return remote_url

def get_all_distros():
    """
    Returns a list of Distro objects.
    Hybrid approach: Uses local assets from src/assets/ if they match the user's filenames,
    otherwise falls back to official internet URLs.
    """
    return [
        # --- NEWBIE (User Friendly) ---
        Distro(
            id="ubuntu", 
            name="Ubuntu 24.04 LTS", 
            description=(
                "Ubuntu is the most widely used Linux distribution in the world, known for its polish, stability, and massive community support. "
                "Version 24.04 'Noble Numbat' brings the modern GNOME 46 desktop, enhanced gaming performance, and 5 years of free security updates. "
                "It's the perfect starting point for anyone new to Linux, offering a 'just works' experience with vast software availability."
            ),
            logo_resource="ubuntu", 
            website="https://ubuntu.com", 
            download_url="https://releases.ubuntu.com/24.04/ubuntu-24.04.3-desktop-amd64.iso", 
            logo_url=get_asset("ubuntu-logo.png", "https://upload.wikimedia.org/wikipedia/commons/a/ac/Ubuntu2022.svg"),
            screenshot_urls=[
                get_asset("ubuntu-screenshot.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e0/Ubuntu_24.04.png"),
            ],
            desktop_environment="GNOME", 
            base="Debian", 
            tags=["Newbie", "Stable", "Popular"]
        ),
        Distro(
            id="linuxmint", 
            name="Linux Mint 22", 
            description=(
                "Linux Mint is designed to work out of the box and is fully equipped with the apps most people need. "
                "Its flagship Cinnamon desktop provides a familiar, Windows-like layout with a Start menu and taskbar, making it the easiest transition for former Windows users. "
                "Prioritizing elegance and comfort, Mint gives you a powerful system without the learning curve."
            ),
            logo_resource="linuxmint", 
            website="https://linuxmint.com", 
            download_url="https://mirrors.edge.kernel.org/linuxmint/stable/22/linuxmint-22-cinnamon-64bit.iso", 
            logo_url=get_asset("linuxmint_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/3/3f/Linux_Mint_logo_without_wordmark.svg"),
            screenshot_urls=[
                get_asset("linuxmint-screenshot.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/07/Linux_Mint_22_Cinnamon.png"),
            ],
            desktop_environment="Cinnamon", 
            base="Ubuntu", 
            tags=["Newbie", "Windows-like", "Stable"]
        ),
        Distro(
            id="zorin", 
            name="Zorin OS 17", 
            description=(
                "Zorin OS is the privacy-focused alternative to Windows and macOS, designed to make your computer faster, more powerful, and secure. "
                "It features a stunningly beautiful interface that can mimic Windows 11, Mac, or classic Linux layouts with a single click. "
                "Included tools allow you to run many Windows apps seamlessly."
            ),
            logo_resource="zorin", 
            website="https://zorin.com/os/download/", 
            download_url="", 
            logo_url=get_asset("zorinos-logo.png", "https://upload.wikimedia.org/wikipedia/commons/8/87/Zorin_Logomark.svg"),
            screenshot_urls=[
                get_asset("zorinos-shot.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/30/Zorin_OS_17_Core_Desktop.png")
            ],
            desktop_environment="GNOME (Modified)", 
            base="Ubuntu", 
            tags=["Newbie", "Beautiful", "Mac-like"]
        ),
        Distro(
            id="popos", 
            name="Pop!_OS", 
            description=(
                "Pop!_OS is an operating system for STEM and creative professionals who use their computer as a tool to discover and create. "
                "It features advanced window tiling, workspace management, and out-of-the-box support for Nvidia graphics. "
                "Created by System76, it's optimized for performance and developer workflows."
            ),
            logo_resource="pop-os", 
            website="https://pop.system76.com", 
            download_url="", 
            logo_url=get_asset("popos_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/4/46/Pop%21_OS_Icon.svg"),
            screenshot_urls=[
                 get_asset("popos_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/7/77/Pop_OS_22.04_Desktop.png")
            ],
            desktop_environment="COSMIC", 
            base="Ubuntu", 
            tags=["Newbie", "Gaming", "Developer"]
        ),
        Distro(
            id="elementary", 
            name="elementary OS 7", 
            description=(
                "The thoughtful, capable, and ethical replacement for Windows and macOS. "
                "elementary OS emphasizes strict design guidelines, privacy, and a pay-what-you-can app store. "
                "Its Pantheon desktop is simple, fast, and incredibly polished, feeling very similar to macOS."
            ),
            logo_resource="elementary", 
            website="https://elementary.io", 
            download_url="https://archive.org/download/elementaryos-7.0-stable.20230129rc_202303/elementaryos-7.0-stable.20230129rc.iso", 
            logo_url=get_asset("elementary-logo.jpg", "https://upload.wikimedia.org/wikipedia/commons/d/d7/Elementary_OS_logo.svg"),
            screenshot_urls=[
                get_asset("elementary_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/0/03/Elementary_OS_7_Desktop.png")
            ],
            desktop_environment="Pantheon", 
            base="Ubuntu", 
            tags=["Newbie", "Mac-like", "Minimal"]
        ),

        # --- CUSTOMIZABLE (Intermediate/Advanced/Riceable) ---
        Distro(
            id="arch", 
            name="Arch Linux", 
            description=(
                "A lightweight and flexible Linux distribution that truly adheres to the KISS (Keep It Simple, Stupid) principle. "
                "You start with a command line and build your system piece by piece. "
                "It features a Rolling Release model, meaning you install once and update forever, always having the absolute latest software."
            ),
            logo_resource="archlinux", 
            website="https://archlinux.org", 
            download_url="https://geo.mirror.pkgbuild.com/iso/latest/archlinux-x86_64.iso", 
            logo_url=get_asset("arch_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/a/a5/Arch_Linux_logo.svg"),
            screenshot_urls=[
                 get_asset("arch_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/f/f3/Arch_Linux_KDE_Plasma.png")
            ],
            desktop_environment="None (DIY)", 
            base="Arch", 
            tags=["Customizable", "DIY", "Rolling"]
        ),
        Distro(
            id="manjaro", 
            name="Manjaro", 
            description=(
                "Manjaro provides all the benefits of Arch Linux (speed, latest software) but wraps it in a user-friendly installer and stable updates. "
                "It makes the 'scary' Arch world accessible to everyone, with pre-configured desktops and graphical tools for driver management."
            ),
            logo_resource="manjaro", 
            website="https://manjaro.org/download/", 
            download_url="", 
            logo_url=get_asset("manjaro_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/3/3e/Manjaro-logo.svg"),
            screenshot_urls=[
                get_asset("manjaro_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/d/d4/Manjaro_24.0_Wynshtoke_KDE_Plasma.png")
            ],
            desktop_environment="KDE/GNOME/XFCE", 
            base="Arch", 
            tags=["Customizable", "Rolling", "Gaming"]
        ),
        Distro(
            id="fedora", 
            name="Fedora Workstation 41", 
            description=(
                "Fedora is the upstream testing ground for Red Hat Enterprise Linux. It showcases the future of the Linux desktop "
                "with the pure, unmodified GNOME interface and cutting-edge technologies like PipeWire and Wayland. "
                "It's widely used by developers (especially Linux kernel devs) for its robust engineering."
            ),
            logo_resource="fedora", 
            website="https://fedoraproject.org", 
            download_url="https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.4.iso", 
            logo_url=get_asset("fedora_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/4/41/Fedora_icon_%282021%29.svg"),
             screenshot_urls=[
                get_asset("fedora_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/a/a1/Fedora_Workstation_40_Desktop.png")
            ],
            desktop_environment="GNOME", 
            base="Fedora", 
            tags=["Customizable", "Developer", "Bleeding Edge"]
        ),
        Distro(
            id="nixos", 
            name="NixOS", 
            description=(
                "NixOS allows you to configure your entire operating system in a single text file. "
                "If an update breaks something, you can rollback to the previous version largely instantly from the boot menu. "
                "It has a steep learning curve but offers unmatched reliability and reproducibility."
            ),
            logo_resource="nixos", 
            website="https://nixos.org", 
            download_url="https://channels.nixos.org/nixos-25.11/latest-nixos-gnome-x86_64-linux.iso", 
            logo_url=get_asset("nixos-logo.png", "https://upload.wikimedia.org/wikipedia/commons/2/28/NixOS_logo.svg"),
            screenshot_urls=[
                 get_asset("nixos-screenshot.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1d/NixOS_24.05_Gnome.png")
            ],
            desktop_environment="Various", 
            base="Nix", 
            tags=["Customizable", "Immutable", "Advanced"]
        ),
        # --- CLASSICS (Server/Enterprise/Old School) ---
        Distro(
            id="debian", 
            name="Debian 12 'Bookworm'", 
            description=(
                "Debian is the 'Universal Operating System' and the grandmother of half the Linux internet (including Ubuntu). "
                "It prizes stability and Free Software principles above all else. "
                "Debian Stable is rock solid and changes very slowly, making it perfect for servers and critical workstations."
            ),
            logo_resource="debian", 
            website="https://debian.org", 
            download_url="https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso", 
            logo_url=get_asset("png-clipart-debian-arch-linux-computer-icons-desktop-linux-spiral-logo.png", "https://upload.wikimedia.org/wikipedia/commons/4/4a/Debian-OpenLogo.svg"),
            screenshot_urls=[
                get_asset("debian_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/f/f6/Debian_12_GNOME_Desktop.png")
            ],
            desktop_environment="Various", 
            base="Debian", 
            tags=["Classics", "Stable", "Server"]
        ),
        Distro(
            id="opensuse", 
            name="openSUSE Tumbleweed", 
            description=(
                "A community project sponsored by SUSE. Tumbleweed is their rolling release version that is automatically tested by OpenQA to ensure stability. "
                "It features YaST, a comprehensive system administration tool that handles everything from partitioning to firewall settings graphically."
            ),
            logo_resource="opensuse", 
            website="https://opensuse.org", 
            download_url="https://download.opensuse.org/tumbleweed/iso/openSUSE-Tumbleweed-DVD-x86_64-Current.iso", 
            logo_url=get_asset("opensuse_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/d/d0/OpenSUSE_Logo.svg"),
            screenshot_urls=[
                 get_asset("opensuse_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/7/76/KDE_Plasma_6_screenshot_%28openSUSE_dark_mode%29.png")
            ],
            desktop_environment="KDE Plasma 6", 
            base="SUSE", 
            tags=["Classics", "Rolling", "SysAdmin"]
        ),
        Distro(
            id="slackware", 
            name="Slackware", 
            description=(
                "Launched in 1993, Slackware is the oldest surviving Linux distro. It attempts to be as 'Unix-like' as possible. "
                "It has no dependency resolution in its package manager. You are the dependency resolver. "
                "Using Slackware is the ultimate way to learn exactly how Linux works under the hood."
            ),
            logo_resource="slackware", 
            website="http://www.slackware.com", 
            download_url="https://mirrors.slackware.com/slackware/slackware-iso/slackware64-15.0-iso/slackware64-15.0-install-dvd.iso", 
            logo_url=get_asset("Slackware_logo.png", "https://upload.wikimedia.org/wikipedia/commons/2/22/Slackware_Logo.svg"),
            screenshot_urls=[
                get_asset("slackware_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/3/30/Slackware_15.0_KDE_Plasma_Desktop.png")
            ],
            desktop_environment="KDE/XFCE", 
            base="Slackware", 
            tags=["Classics", "Difficult", "Old School"]
        ),
        Distro(
            id="gentoo", 
            name="Gentoo", 
            description=(
                "Gentoo is a source-based distribution. You don't install programs; you compile them from source code on your own machine. "
                "This allows for extreme optimization for your specific hardware. "
                "Not for the faint of heart, but powerful for those who need absolute control."
            ),
            logo_resource="gentoo", 
            website="https://gentoo.org", 
            download_url="https://distfiles.gentoo.org/releases/amd64/autobuilds/current-install-amd64-minimal/install-amd64-minimal-20251214T170402Z.iso", 
            logo_url=get_asset("Gentoo_Linux_logo_matte.png", "https://upload.wikimedia.org/wikipedia/commons/4/41/Gentoo-logo.svg"),
            screenshot_urls=[
                get_asset("gentoo_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/a/a4/Gentoo_LiveGUI_2024.png")
            ],
            desktop_environment="None", 
            base="Gentoo", 
            tags=["Classics", "Source-based", "Hardcore"]
        ),
         Distro(
            id="kali", 
            name="Kali Linux", 
            description=(
                "Funded and maintained by Offensive Security, Kali is the industry standard for penetration testing and security auditing. "
                "It comes packed with hundreds of tools for hackers and security professionals. "
                "It is NOT recommended as a daily driver for general use."
            ),
            logo_resource="kali", 
            website="https://kali.org", 
            download_url="https://cdimage.kali.org/current/kali-linux-2025.4-installer-amd64.iso", 
            logo_url=get_asset("kali_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/4/4b/Kali_Linux_2.0_wordmark.svg"),
             screenshot_urls=[
                get_asset("kali-screenshot.jpg", "https://upload.wikimedia.org/wikipedia/commons/8/8b/Kali_Linux_2024.1_Desktop.png")
            ],
            desktop_environment="XFCE", 
            base="Debian", 
            tags=["Classics", "Security", "Hacking"]
        ),
        Distro(
            id="void", 
            name="Void Linux", 
            description=(
                "Void is a general-purpose operating system, based on the monolithic Linux kernel. "
                "It is one of the few independent distros not based on Debian, Fedora, or Arch. "
                "Known for its speed and its own package manager (XBPS) and init system (runit)."
            ),
            logo_resource="void", 
            website="https://voidlinux.org", 
            download_url="https://repo-default.voidlinux.org/live/current/void-live-x86_64-musl-20250202-base.iso", 
            logo_url=get_asset("void_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/0/02/Void_Linux_logo.svg"),
            screenshot_urls=[
                get_asset("void-cosmic-desktop.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c1/VoidLinux_Xfce_Desktop.png")
            ],
            desktop_environment="XFCE/None", 
            base="Independent", 
            tags=["Customizable", "Independent", "Fast"]
        ),

        # --- PROPRIETARY (Reference / Restoration) ---
        Distro(
            id="windows11", 
            name="Windows 11", 
            description=(
                "The latest operating system from Microsoft. Known for its centrally centered taskbar and compatibility with virtually all PC software. "
                "Included here for restoration purposes or for those who need to dual-boot. "
                "Requires a valid license key for full functionality."
            ),
            logo_resource="windows", 
            website="https://www.microsoft.com/software-download/windows11", 
            download_url="", # Direct link not possible
            logo_url=get_asset("windows_logo.svg", "https://upload.wikimedia.org/wikipedia/commons/e/e6/Windows_11_logo.svg"),
            screenshot_urls=[
                get_asset("windows_screenshot.png", "https://upload.wikimedia.org/wikipedia/commons/d/d7/Windows_11_screenshot.png")
            ],
            desktop_environment="Flux", 
            base="NT", 
            tags=["Proprietary", "Standard", "Gaming"]
        ),
    ]
