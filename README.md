# Installation 
1. git clone the repo
2. Install the folowing packages:
	> pip install fastapi
	> pip install "uvicorn[standard]"
2. Make sensors_api.py run on startup. I use a systemctl service, as shown below.

`[Unit]
Description=VM Temp API
[Service]
ExecStart=<python_location> /<path_to_script>/vmhost_sensors_api.py
User=<user> # this is required else the script will run as admin and fail due to not finding the module>
[Install]
WantedBy=multi-user.target
`

3. Add the xbar_vmhost_sensors_plugin to xbar.

# Configuration
The default API port is 8004, you can change it in vmhost_sensors_api.py if needed, remember to update the variable LOCAL_PORT in the plugin file as well . You will also need to update LOCAL_IP variable in the plugin file, so it matches your system one. 

Currently there are 2 layouts/groupings available, one is by_measurement_type ("v2") the other is by_adapter ("v1"). You can switch between them by editing the LAYOUT_TYPE variable in the plugin file.