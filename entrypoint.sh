#!/bin/bash

arduino-cli core install arduino:avr
arduino-cli compile --fqbn arduino:avr:uno arduino_module/src
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno arduino_module/src