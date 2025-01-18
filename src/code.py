import os
import time
from display import Display
from connectionManager import ConnectionManager
from buttons import Buttons
from menus import Menus



def read_version():
	""" Read the current version of the software """
	with open('/version.txt') as fp:
		version = fp.readline()
		version = version.rstrip()
		return version
	return None



#
# MAIN
#

# Read the current version of the software
version = read_version()

# Read settings.toml
connection_method	= os.getenv("CONNECTION_METHOD")
onstepx_wifi_ssid	= os.getenv("ONSTEPX_WIFI_SSID")
onstepx_wifi_password	= os.getenv("ONSTEPX_WIFI_PASSWORD")
onstepx_ip_addr		= os.getenv("ONSTEPX_IP_ADDR")
onstepx_port		= os.getenv("ONSTEPX_PORT")
display_color		= os.getenv("DISPLAY_COLOR")
info_text		= os.getenv("INFO_TEXT")

# Start the display
display = Display(version, display_color, info_text)

buttons			= Buttons()
connection_manager	= ConnectionManager(connection_method, onstepx_wifi_ssid, onstepx_wifi_password, onstepx_ip_addr, onstepx_port, debug=False)
menus			= Menus(connection_manager, version, info_text)

connection_manager.connect()

while True:
	if connection_manager.connected():
		"""
		ra = send_command('GR', reply_expected = True)
		dec = send_command('GD', reply_expected = True)
		az = send_command('GZ', reply_expected = True)
		alt = send_command('GA', reply_expected = True)
		display.display_position(ra, dec, az, alt)
		"""

		# Read Buttons
		(buttonsPressed, buttonsReleased, buttonsHeld) = buttons.process()
		menus.process_buttons(buttonsPressed, buttonsReleased, buttonsHeld)

		if menus.needs_redisplay():
			lines = menus.get_menu_display()
			display.display_menu(lines)
	else:
 		display.display_connecting(connection_method, onstepx_wifi_ssid)
		connection_manager.connect()

	# Read OnStepX Controller

	# Write OnStepX Controller
	
	# Update Display

	#time.sleep(0.1)
