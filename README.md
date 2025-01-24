
<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/adrianlavery/pi-web-watcher">
    <img src="images/logo.png" alt="Logo" width="100" height="100">
  </a>

<h3 align="center">Pi Web Watcher</h3>

  <p align="center">
    Real-Time Web Monitoring with Raspberry Pi
    <br />
    <br />
    <a href="#contributing">Contribute</a>
    &middot;
    <a href="https://github.com/adrianlavery/pi-web-watcher/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/adrianlavery/pi-web-watcher/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Lifeboat crew on rear deck (c) Nigel Millard][lifeboat-crew]

I have volunteered with the [RNLI](https://rnli.org/) since 2007 and have always sought to leverage my tech background to assist our station. Recently, we've been using a Raspberry Pi to run a display screen that shows information such as weather, tides, and local charts with marine traffic using AIS. However, the display (an LG TV) is also used for other purposes, and switching the HDMI port to the Pi can be time-consuming, especially during emergencies when every second counts.

To address this, I explored various methods to automate the HDMI channel switching, including reacting to text or email alerts when we are launched on service. However, these solutions had multiple dependencies, making them complex. I prefer simplicity. The RNLI uses a system called RCAMS (RNLI Callout and Messaging System) alongside a pager system to contact volunteer crew for emergency responses. This same system is also used to track crewing levels and is already displayed on our station's screen.

I decided to utilize RCAMS to monitor for launch alerts and automatically switch the HDMI channel. This solution allows us to run everything from the Pi without relying on email or text messages. At it's core, is a python script that uses Selenium to check the text on a webpage. In my case, the text is "No live incidents". If this text is not present, due to an ongoing incident, then we use CEC to activate the display.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![RaspberryPi][RaspberryPi]][RaspberryPi-url]
* [![Python][Python]][Python-url]
* [![dotEnv][dotEnv]][dotEnv-url]
* [![Selenium][Selenium]][Selenium-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you can get this up and running on your own Raspberry Pi, monitoring any website you want.

### Prerequisites

This is what you'll need to install on your Raspberry Pi.

    ```
    # Python
    sudo apt-get install python3
    # Python Package Installer
    sudo apt-get install python3-pip
    # Chrome Web Driver
    sudo apt install chromium-chromedriver
    # CEC Utils
    sudo apt-get install cec-utils
    # .Env
    pip install python-dotenv
    # Selenium
    pip install selenium==4.27.0
    ```

### Installation

1. SSH into your Raspberry Pi
2. Clone the repo
   ```sh
   git clone https://github.com/adrianlavery/pi-web-watcher.git
   ```
3. Update `./src/config.env` with your specific scenario
   ```sh
   # This is the website you want to monitor
   URL=https://www.example.com/
   # This is the text you want to monitor on the website
   QUERY_TEXT='Example Text'
   # This is the XPath to the element on the webpage containing your query text
   QUERY_TEXT_XPATH='//*[@id="exampleApp"]/div[5]/div/div[1]/div/h5/span'
   # This is the username and password to login to the site
   LOGIN_USER=username
   LOGIN_PASS=password
   # This is name of the logfile
   LOG_FILE=monitorWebsite.log
   ```
4. Test your script is working by running `python3 ./src/monitorWebsite.py`. The log file will be created in `./src/logs/`. You can cat the logfile to see the output.
   ```
   2025-01-23 17:58:36,805 - Starting...
   2025-01-23 17:58:36,805 - Opening https://www.example.com/
   2025-01-23 17:58:38,555 - Logging in
   2025-01-23 17:58:42,937 - Login successful
   2025-01-23 17:59:12,967 - Checking for 'Example Text' every 30 seconds...
   ```
   Be aware that the script runs in a constant loop so you will have to `ctrl+c` to exit.
5. Create a service to run the script in the background when the pi boots. Update the file `./src/monitor_website.service` to reflect the location of your script and the user account that the service will run under.
   ```sh
    [Unit]
    Description=Monitor Website Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /home/pi/monitorWebsite/src/monitorWebsite.py # python script
    WorkingDirectory=/home/pi/monitorWebsite/src/ # working directory
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=pi # User account that the service runs under

    [Install]
    WantedBy=multi-user.target
   ```
6. Create a symbolic link to `./src/monitor_website.service` in `/etc/systemd/system`.
   ```sh
    # Create the link
    ln -s ./src/monitor_website.service /etc/systemd/system/monitor_website.service
    # Enable the service
    sudo systemctl enable monitor_website.service
    # Start the service
    sudo systemctl start monitor_website.service
    # Check the service status
    sudo systemctl status monitor_website.service
   ```
   Log files will be in the `./logs` directory as before.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Make the website login an option as not all websites will require a login
- [ ] Remove the requirement for login details in plain text in the config file
- [ ] Make the default 30s timing loop configurable to allow for websites that don't change very often
- [ ] Make the element types and id values configurable

See the [open issues](https://github.com/adrianlavery/pi-web-watcher/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/adrianlavery/pi-web-watcher/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=adrianlavery/pi-web-watcher" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Adrian Lavery - [![bluesky][bluesky]][bluesky-url]  [![linkedin][linkedin]][linkedin-url]

Project Link: [https://github.com/adrianlavery/pi-web-watcher](https://github.com/adrianlavery/pi-web-watcher)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* I found this gist by [Gordon Turner](https://github.com/rmtsrc) after struggling for quite a bit controlling CEC, which luckliy had all the answers 😂 -  [Using cec-client on a Raspberry Pi](https://gist.github.com/rmtsrc/dc35cd1458cd995631a4f041ab11ff74)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/adrianlavery/pi-web-watcher.svg?style=for-the-badge
[contributors-url]: https://github.com/adrianlavery/pi-web-watcher/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/adrianlavery/pi-web-watcher.svg?style=for-the-badge
[forks-url]: https://github.com/adrianlavery/pi-web-watcher/network/members
[stars-shield]: https://img.shields.io/github/stars/adrianlavery/pi-web-watcher.svg?style=for-the-badge
[stars-url]: https://github.com/adrianlavery/pi-web-watcher/stargazers
[issues-shield]: https://img.shields.io/github/issues/adrianlavery/pi-web-watcher.svg?style=for-the-badge
[issues-url]: https://github.com/adrianlavery/pi-web-watcher/issues
[license-shield]: https://img.shields.io/github/license/adrianlavery/pi-web-watcher.svg?style=for-the-badge
[license-url]: https://github.com/adrianlavery/pi-web-watcher/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin]: https://img.shields.io/badge/LinkedIn-grey?logo=linkedin
[linkedin-url]: https://linkedin.com/in/adrianlavery
[product-screenshot]: images/screenshot.png
[lifeboat-crew]: images/lifeboat_crew.jpg

[Python]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff
[Python-url]: https://www.python.org/
[Selenium]: https://img.shields.io/badge/Selenium-43B02A?logo=selenium&logoColor=fff
[Selenium-url]: https://www.selenium.dev/
[RaspberryPi]: https://img.shields.io/badge/Raspberry%20Pi-red?logo=raspberrypi
[RaspberryPi-url]: https://www.raspberrypi.com/
[dotEnv]: https://img.shields.io/badge/.ENV-yellow?logo=dotenv
[dotEnv-url]: https://www.dotenv.org/
[bluesky]: https://img.shields.io/badge/Bluesky-grey?logo=bluesky
[bluesky-url]: https://bsky.app/profile/adrianlavery.bsky.social