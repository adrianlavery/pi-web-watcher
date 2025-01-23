# Install on Raspberry Pi

## Requirements

sudo apt-get install python3-pip
sudo apt install chromium-chromedriver
sudo apt-get install cec-utils
sudo apt-get install python3-tk
pip install python-dotenv
pip install selenium==4.27.0

## Copy the source
Copy the files `src/config.env` and `src/monitorWebsite.py` to your pi. The files can go anywhere in the file system, e.g. `~/monitorWebsite`.

## Configure
Update `config.env` to reflect your scenario.
```
URL=https://www.example.com/
QUERY_TEXT='Example Text'
QUERY_TEXT_XPATH='//*[@id="exampleApp"]/div[5]/div/div[1]/div/h5/span'
LOGIN_USER=username
LOGIN_PASS=password
LOG_FILE=monitorWebsite.log
```
Note that the username and password in this scenario are held in this file in open text so use this example with caution!

### Test script
You can test the script at this point by simply running `python3 monitorWebsite.py`. The log file will be created in ./logs of the working folder. You can cat the logfile to see the output. 
```
2025-01-23 17:58:36,805 - Starting...
2025-01-23 17:58:36,805 - Opening https://www.example.com/
2025-01-23 17:58:38,555 - Logging in
2025-01-23 17:58:42,937 - Login successful
2025-01-23 17:59:12,967 - Checking for 'Example Text' every 30 seconds...
```
Be aware that it runs on a constant loop so you will have to manually close the script.

## Create Service
Now that the script is working, you can create a new service on your pi so that the script will run in the background when the pi boots.   
Update the file `monitor_website.service` to reflect the location of your script and the user account that the servcie will run under.

```
[Unit]
Description=Monitor Website Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/monitorWebsite/monitorWebsite.py
WorkingDirectory=/home/pi/monitorWebsite
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Copy the file to `/etc/systemd/system/`.  
Run the following commands
```
sudo systemctl enable monitor_website.service
sudo systemctl start monitor_website.service
sudo systemctl status monitor_website.service
```

The service will auto start on boot and run the script. Log files will be in the `./logs` directory.