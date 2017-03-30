# Epson SDP Replacement

As i've had printers (tm-V88V) which are not enabled to use SDP,
i wrote this simple python script and let it run on an *pi zero w* in the same network as the printer.

# USAGE

One needs to set some env vars.

- PRINTER_ID
- PRINTER_IP
- SERVER_URL
- SERVER_AUTH_TOKEN

# SETUP

## Systemctl

Step 2 – Create A Unit File

Next we will create a configuration file (aka a unit file) that tells systemd what we want it to do and when :

sudo nano /lib/systemd/system/myscript.service
Add in the following text :

[Unit]
Description=EPSON SDP Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/epson_sdp_script.py

[Install]
WantedBy=multi-user.target
You can save and exit the nano editor using [CTRL-X], [Y] then [ENTER].

This defines a new service called “My Script Service” and we are requesting that it is launched once the multi-user environment is available. The “ExecStart” parameter is used to specify the command we want to run. The “Type” is set to “idle” ensures the ExecStart command is only run when everything else has loaded. For my GPIO based scripts the default type of “simple” didn’t work.

Note that the paths are absolute and fully define the location of Python as well as the location of our Python script.

In order to store the script’s text output in a log file you can change the ExecStart line to :

ExecStart=/usr/bin/python /home/pi/myscript.py > /home/pi/myscript.log 2>&1
The permission on the unit file needs to be set to 644 :

sudo chmod 644 /lib/systemd/system/myscript.service
Step 3 – Configure systemd

Now the unit file has been defined we can tell systemd to start it during the boot sequence :

sudo systemctl daemon-reload
 sudo systemctl enable myscript.service
Reboot the Pi and your custom service should run :

sudo reboot
Step 4 – Check status of your service

You can check the status of your service using :

sudo systemctl status myscript.service

[Source](http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/)