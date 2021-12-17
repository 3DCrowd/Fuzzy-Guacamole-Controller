
# Fuzzy Guacamole Controller

Fuzzy Guacamole Controller is a custom Raspberry Pi OS designed to make 3D printing as user friendly and trouble free as possible. It provides a web interface for uploading and executing print jobs on any 3d printer that runs Marlin firmware.

## Supported technologies
Fuzzy Guacamole Controller has only been tested on the Raspberry Pi 4 but it should work on all the currently released pis. It has been tested on 3d printers running Marlin 1 and Marlin 2 firmware.

## Installation

Install Fuzzy Guacamole Controller using either the install script or custom image.

### Install from install script
**Step 1**\
Open your pi's terminal.

**Step 2**\
Download the latest `install.sh` file using the following command:
```bash
wget https://github.com/3DCrowd/Fuzzy-Guacamole-Controller/releases/download/v0.1.0/install.sh
```

**Step 3**\
Mark the install script as executable.
```bash
sudo chmod +x install.sh
```

**Step 4**\
Run the install script
```bash
sudo ./install.sh
```

**Step 5**\
Restart your pi
```bash
sudo reboot
```

**Step 6**\
Finally, connect the pi to the printer with a suitable usb cable and select the port on the Fuzzy Guacamole Dashboard to see the connected printers controls.


### Install from custom image.
**Step 1**\
Download the latest version of [Balena Etcher](https://www.balena.io/etcher/).

**Step 2**\
Download the latest Fuzzy Guacamole `.img.xz` file from the [releases tab](https://github.com/3DCrowd/fuzzy-guacamole/releases/).

**Step 3**\
Use Balena Etcher to burn the latest image to the sd card.

**Step 4**\
If you are planning on connecting to the printer over wifi create a `wpa_supplicant.conf` as outlined [here](https://www.raspberrypi.org/documentation/computers/configuration.html#configuring-networking-2) and place it in the boot partion of the sd card.

(Note: This step is not required if using a wired ethernet connection).

**Step 5**\
Plug the sd card into the pi and connect it to power. After a few minutes you should be able to access it by navigating to [http://fuzzyguacamole.local](http://fuzzyguacamole.local) when connected to the same wifi network.

**Step 6**\
Finally, connect the pi to the printer with a suitable usb cable and select the port on the Fuzzy Guacamole Dashboard to see the connected printers controls.

## Usage

**Step 1**\
Connect your 3D printer to your pi using a suitable usb cable.

**Step 2**\
Navigate to [http://fuzzyguacamole.local](http://fuzzyguacamole.local) while connected to the same wifi network that your pi is connected to.

**Step 2**\
Select the port of your printer from the dropdown and select *Try Again With This Port* to access the dashboard. 

**Step 3**\
Drag and drop your `.gcode` files into the upload gcode panel and hit print to send the file to the printer.
## Screenshots

![Could Not Connect Message](https://github.com/3DCrowd/fuzzy-guacamole/raw/main/readme_img/could_not_connect.png)
![Fuzzy Guacamole Dashboard](https://github.com/3DCrowd/fuzzy-guacamole/raw/main/readme_img/dashboard.png)
## Roadmap

- Support for local slicing

- Dashboard Customisation

- User friendly connection to wifi

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

