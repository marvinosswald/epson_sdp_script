# Epson SDP Replacement

As i've had printers (tm-V88V) which are not enabled to use SDP,
i wrote this simple python script and let it run on an *pi zero w* in the same network as the printer.

# USAGE

One needs to create a config file

```
[SERVER]
URL = http://myrestaurant.dev
AUTH_TOKEN = de

[PRINTER]
ID = 1
IP = Bondrucker

```

# SETUP

##Permissions
- clone git repo as pi
- chmod a+x relay.py

## Crontab

### 1
* * * * * cd /home/pi/epson_sdp_script && /usr/bin/python /home/pi/epson_sdp_script/relay.py > /home/pi/logs/relay.log 2>&1

### 2
*/5 * * * * /bin/sh -c 'cd /home/pi/epson_sdp_script && /usr/bin/git fetch --all && /usr/bin/git reset --hard origin/release && chmod a+x relay.sh'