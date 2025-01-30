# PyHC

## Introduction

PyHC is a bare-bones Circuit Python implementation of a hand controller for the OnStepX telescope controller. It's designed to leverage the Adafruit ESP32-S2/S3 Feathers with built in displays and chargers, requiring only a battery, switches and an RJ12 port (hardware connection only). It possible to build a hand controller without needing a PCB or many parts.

PyHC will connect to OnStepX via WiFi or ST4. It's designed to provide common simple functionality on the basis that other functionality is accessed infrequently and can be accomplished via other means.

The code is designed to be simple, so is easy to adapt.  Installation is a breeze, being drag and drop.

If you need to build a controller fast, this is likely the quickest method other than purchasing something ready built.

Although PiHC code is a complete write from scratch, it contains catalogs and algorithms derived from:

* [Smart Hand Controller](https://github.com/hjd1964/SmartHandController)
* [Teen Astro](https://github.com/charleslemaire0/TeenAstro)

## Building The Hardware

| Item | GPIO |
| ---- | ---- |
| F1 | GPIO5 |
| F2 | GPIO6 |
| N | GPIO9 |
| S | GPIO10 |
| E |  GPIO11 |
| W | GPIO12 |
| Center |  GPIO8 (A5) |
| Power Switch | EN(if powered by LiPo), USB(if powered by 5V regulator) |
| Power Switch | GND |

Connect the other side of every button switch to GND

If 3 x AA powered, connect Schottky Diode CUS08F30H3FCT in 4.5V from battery (for reverse polarity protection), and use https://www.amazon.ca/dp/B09Z2CVQYQ 5V Buck Boost Power Module to convert battery to 5V.

## 3D Printed Case

## Installing

1. Connect feather via USB to a desktop
2. If the feather is brand new, i.e. Circuit Python has not been installed yet, then:
	* Enter Bootloader Mode: Press reset, pause 1 second, press reset again to enter the Green/Blue/Orange Feather TFT Bootloader mode.  If you fail to enter this mode, try again.
	* A new drive will be av available on your system called something like FTHRS3BOOT
	* Download the latest version .UF2 for Circuit Python for your board from [Circuit Python Downloads](https://circuitpython.org/downloads), pay particular attention that you download for the correct board type
	* Copy the .uf2 to the FTHRS3BOOT drive
	* Congratuations, you now have Circuit Python installed
3. The board will reset automatically, and a new drive CIRCUITPY will become available
4. Edit src/settings.toml and change to your requirements
5. Copy all the files from src onto the top level of the CIRCUITPY drive
6. The board will auto reset and you're ready to connect to OnStep

