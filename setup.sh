#!/bin/bash

echo "Starting setup..."
echo "i2c-bcm2708" > /etc/modules
echo "i2c-dev" > /etc/modules 

apt-get install python-smbus
apt-get install i2c-tools

#
#blacklist spi-bcm2708
#blacklist i2c-bcm2708
#in /etc/modprobe.d/raspi-blacklist.conf
#
