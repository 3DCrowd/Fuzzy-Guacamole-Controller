
# Fuzzy Guacamole Controller

Fuzzy Guacamole Controller is a custom Raspberry Pi OS designed to make printing as user friendly and trouble free as possible.


## Installation

Install Fuzzy Guacamole by installing the latest image to an sd card.

#### Step 1
Download the latest version of [Balena Etcher](https://www.balena.io/etcher/).

#### Step 2
Download the latest Fuzzy Guacamole `.img` file from the [releases tab](https://github.com/3DCrowd/fuzzy-guacamole/releases/).

#### Step 3
Use Balena Etcher to burn the lastest image to the sd card.

#### Step 4
If you are planning on connecting to the printer over wifi create a `wpa_supplicant.conf` as outlined [here](https://www.raspberrypi.org/documentation/computers/configuration.html#configuring-networking31) and place it in the boot partion of the sd card.
(Note: This step is not required if using a wired ethernet connection).

#### Step 5
Plug the sd card into the pi and connect it to power. After a few minutes you should be able to access it by navigating to [fuzzyguacamole.local](http://fuzzyguacamole.local) when connected to the same wifi network.

#### Step 6
Finally, connect the pi to the printer with a suitable usb cable and reload the Fuzzy Guacamole Dashboard to see the connected printers controls.

## Roadmap

- Support for local slicing

- Dashboard Customisation

- User friendly connection to wifi

  
## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

  
