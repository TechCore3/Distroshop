#  DistroShop

**DistroShop** is a modern, beautiful Linux distribution explorer and downloader built with GTK4 and Libadwaita. It provides a seamless interface to browse, discover, and download various Linux distributions.

![App Icon](assets/app_icon.png)

##  Features

- **Explore Distributions**: Browse a curated list of popular Linux distributions with logos and screenshots.
- **Detailed Information**: View distribution summaries, descriptions, and categories.
- **Direct Downloads**: Download ISO files directly within the application.
- **Modern UI**: Vibrant colors, dark mode support, and smooth animations.
- **USB Writing Tools**: Integrated tools to help prepare your installation media.

##  Installation

### Flatpak (Recommended)

The easiest way to install DistroShop on any Linux distribution is via Flatpak.

1.  **Build and install locally**:
    ```bash
    flatpak-builder --user --install --force-clean build io.github.distroshop.DistroShop.yml
    ```
2.  **Run the app**:
    ```bash
    flatpak run io.github.distroshop.DistroShop
    ```

### From Source

To run DistroShop directly from the source code, ensure you have the necessary system libraries installed.

1.  **Install Dependencies**:
    You will need Python 3, GTK4, and Libadwaita development libraries.
    - **Fedora**: `sudo dnf install python3-gobject gtk4 libadwaita`
    - **Ubuntu/Debian**: `sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1`
    - **Arch**: `sudo pacman -S python-gobject gtk4 libadwaita`
2.  **Run the app**:
    ```bash
    python src/main.py
    ```

##  Development

### Prerequisites
- Python 3
- GTK4 & Libadwaita development libraries
- `flatpak-builder` (for packaging)

##  License

This project is licensed under the **MIT License**.

##  Credits

- **Icon**: DistroShop (Thrown together in less than 30 seconds)
- **Data & Assets**: Courtesy of Wikimedia Commons and official distribution websites.
##  Contact

- If any issues are found, please open an issue.
- Feel free to suggest any new distros to be added.
---
*Built with ❤️ for the Linux Community.*
