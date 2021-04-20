#!/bin/bash

# Remove existing downloads and binaries so we can start from scratch.
rm google-chrome-stable_current_amd64.deb
rm chromedriver_linux64.zip
rm -f driver/*

# Install Latest Chrome.
set -ex
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Install Latest ChromeDriver.

CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip ./chromedriver_linux64.zip -d ./driver
rm ./chromedriver_linux64.zip
chmod +x ./driver/chromedriver
