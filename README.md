
# The what and why
When running OSX as a VM, there's no "nice" way of monitoring the host temps (mainly CPU), thus this project. It basically dumps the output of the linux `sensors` command to an API you can consume.

![](https://i.imgur.com/Rx8zNeQ.png)  
For my use, I decided to make a menubar applet using xbar, you can check it out here https://github.com/matryer/xbar if you're not already familiar with it. 

## Installation 
1. Clone the repo
2. Install the folowing packages:
	> pip install fastapi  
	> pip install "uvicorn[standard]"
3. Add the xbar_vmhost_sensors_plugin to xbar.
4. Make vmhost_sensors_api.py run on startup. I use a systemctl service, as shown below.

### Run script on startup

1. Create the service file like so `sudo nano /etc/systemd/system/vmtemp.service`
2. Modify the service file to fit your situation.
```
# Example service: vmtemp.service
[Unit]
Description=VM Temp API

[Service]
ExecStart=<python_location> /<path_to_script>/vmhost_sensors_api.py

User=<user> # this is required else the script will run as admin and fail due to not finding the module>

[Install]
WantedBy=multi-user.target
```
3. Enable the service so it runs on startup `sudo systemctl enable vmtemp`
4. Now run this command to start it `sudo systemctl start vmtemp`

## Configuration

Inside the xbar plugin file you will find these variables.
```
LOCAL_IP = "192.168.0.1"
LOCAL_PORT = "8004"
LAYOUT_TYPE = "v2"
```
- You will need to update LOCAL_IP variable so it matches your system one.
- The default API port (8004) is configured through vmhost_sensors_api.py, you can change it if needed, just remember to update the variable LOCAL_PORT in the plugin file. 
- Currently there are 2 layouts/groupings available, one is [("v1")](./layout_v1.png), the other is by_adapter by_measurement_type [("v2")](./layout_v2.png). You can switch between them by editing the LAYOUT_TYPE variable in the plugin file.