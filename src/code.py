import os
import time
from display import Display
from connectionManager import ConnectionManager



def read_version():
	""" Read the current version of the software """
	with open('/version.txt') as fp:
		version = fp.readline()
		version = version.rstrip()
		return version
	return None


def send_command(cmd):
	(success, rx) = connection_manager.send_command(cmd)
	if success:
		print('✅  %s ' % cmd, end='')
		if rx is not None:
			print('-> %s' % rx)
		else:
			print()
	else:
		print('❌  %s failed' % cmd)
	


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

connection_manager = ConnectionManager(connection_method, onstepx_wifi_ssid, onstepx_wifi_password, onstepx_ip_addr, onstepx_port, debug=False)

connection_manager.connect()

while True:
	if connection_manager.connected():
		display.display_menu()

		send_command('SC01/14/25')
		send_command('SL05:34:00')
		send_command('hR')

		send_command('GR')
		send_command('GD')
		send_command('GZ')
		send_command('GA')
		send_command('Sr05:40:20')
		send_command('Sd+80:20:20')
		send_command('GU')
	else:
 		display.display_connecting(connection_method, onstepx_wifi_ssid)
		connection_manager.connect()

	# Read Buttons

	# Read OnStepX Controller

	# Write OnStepX Controller
	
	# Update Display

	time.sleep(1.0)
