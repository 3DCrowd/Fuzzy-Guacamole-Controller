apt-get update

echo "Installing git..."
apt install git -y

echo "Installing Pip..."
apt install python3-pip -y

echo "Installing Apache..."
apt install apache2 -y

echo "Cloning Fuzzy Guacamole from github..."
git clone https://github.com/3DCrowd/fuzzy-guacamole.git /home/pi/fuzzy-guacamole

echo "Installing python requirements..."
pip3 install -r /home/pi/fuzzy-guacamole/requirements.txt

echo "Copying frontend into Apache server..."
cp -r /home/pi/fuzzy-guacamole/src/frontend/. /var/www/html/

echo "Creating API service..."
rm -f /etc/systemd/system/fuzzy-guacamole.service
echo "[Unit]" >> /etc/systemd/system/fuzzy-guacamole.service
echo "Description=Connecting to the printer and starting the API" >> /etc/systemd/system/fuzzy-guacamole.service
echo "After=network.target" >> /etc/systemd/system/fuzzy-guacamole.service
echo "StartLimitIntervalSec=0" >> /etc/systemd/system/fuzzy-guacamole.service

echo "[Service]" >> /etc/systemd/system/fuzzy-guacamole.service
echo "Type=simple" >> /etc/systemd/system/fuzzy-guacamole.service
echo "User=pi" >> /etc/systemd/system/fuzzy-guacamole.service
echo "ExecStart=/usr/bin/python3 /home/pi/fuzzy-guacamole/src/apiController.py" >> /etc/systemd/system/fuzzy-guacamole.service 

echo "[Install]" >> /etc/systemd/system/fuzzy-guacamole.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/fuzzy-guacamole.service

systemctl enable fuzzy-guacamole.service

echo "Creating directories..."
mkdir /home/pi/fuzzy-guacamole/logs
mkdir /home/pi/fuzzy-guacamole/files

chown pi /home/pi/fuzzy-guacamole/logs
chown pi /home/pi/fuzzy-guacamole/files

echo "Creating UDEV rules..."
rm -f /usr/local/bin/fuzzy-guacamole-trigger.sh
echo "#!/usr/bin/bash" >> /usr/local/bin/fuzzy-guacamole-trigger.sh
echo "systemctl restart fuzzy-guacamole.service" >> /usr/local/bin/fuzzy-guacamole-trigger.sh
chmod +x /usr/local/bin/fuzzy-guacamole-trigger.sh

rm -f /etc/udev/rules.d/90-fuzzy-guacamole.rules
echo 'SUBSYSTEM=="usb", ACTION=="add", RUN+="/usr/local/bin/fuzzy-guacamole-trigger.sh"' >> /etc/udev/rules.d/90-fuzzy-guacamole.rules

echo "Changing hostname..."
hostnamectl set-hostname fuzzyguacamole
sed -i "6s/.*/127.0.1.1       fuzzyguacamole/" /etc/hosts

echo "Installing mjpg_streamer..."
apt-get install cmake libjpeg8-dev
git clone https://github.com/jacksonliam/mjpg-streamer /home/pi/mjpg-streamer
cd /home/pi/mjpg-streamer/mjpg-streamer-experimental
make
make install
cd

echo "Creating mjpg_streamer start script..."
rm -f /usr/local/bin/startCamera.sh
echo "#!/usr/bin/bash" >> /usr/local/bin/startCamera.sh
echo "export LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer-experimental/." >> /usr/local/bin/startCamera.sh
echo "/home/pi/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -o 'output_http.so -w ./www' -i 'input_uvc.so'" >> /usr/local/bin/startCamera.sh
chmod +x /usr/local/bin/startCamera.sh

echo "Creating mjpg_streamer service..."
rm -f /etc/systemd/system/startCameraStreamer.service
echo "[Unit]" >> /etc/systemd/system/startCameraStreamer.service
echo "Description=Connecting to the printer and starting the API" >> /etc/systemd/system/startCameraStreamer.service
echo "After=network.target" >> /etc/systemd/system/startCameraStreamer.service
echo "StartLimitIntervalSec=0" >> /etc/systemd/system/startCameraStreamer.service

echo "[Service]" >> /etc/systemd/system/startCameraStreamer.service
echo "Type=simple" >> /etc/systemd/system/startCameraStreamer.service
echo "User=pi" >> /etc/systemd/system/startCameraStreamer.service
echo "ExecStart=/usr/local/bin/startCamera.sh" >> /etc/systemd/system/startCameraStreamer.service
echo "Restart=on-failure" >> /etc/systemd/system/startCameraStreamer.service
echo "RestartSec=10s" >> /etc/systemd/system/startCameraStreamer.service

echo "[Install]" >> /etc/systemd/system/startCameraStreamer.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/startCameraStreamer.service
systemctl enable startCameraStreamer.service

echo "Installation Complete. Please restart before using."

