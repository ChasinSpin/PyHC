import time
import wifi
import ipaddress
import socketpool



class ConnectionManager():

	WIFI_CONNECTION_RETRY_TIME	= 5
	SOCKET_TIMEOUT			= None
	MAX_RX_SIZE			= 25

        def __init__(self, connection_method, wifi_ssid = None, wifi_password = None, ip_addr = None, port = None, debug = False):
		""" connection_method can be either wifi or st4 (in which case wifi_ssid and wifi_password are ignored) """

		self.con_type	= connection_method
		self.debug	= debug

		if self.con_type == 'wifi':
			# Connect to wifi
			self.wifi_ssid				= wifi_ssid
			self.wifi_password			= wifi_password
			self.ip_addr				= ip_addr
			self.port				= port
                	self.wifi_never_connected		= True
                	self.wifi_last_connection_attempt	= -1
			self.socket				= None
		elif self.con_type == 'st4':
			self.connect_st4()
		else:
			raise ValueError("CONNECTION_TYPE must be 'wifi' or 'st4' in settings.toml")


	def connected(self):
		if self.con_type == 'wifi':
			if wifi.radio.connected and self.socket is not None:
				return True
		elif self.con_type == 'st4':
			pass

		return False

	
	def connect_wifi(self):
                """ Connect via wifi. IMPORTANT: Wifi automatically reconnects if it's already connected at least once, so this doesn't need to be called again if there has been a previous success """

                if (time.monotonic() - self.wifi_last_connection_attempt) < self.WIFI_CONNECTION_RETRY_TIME:
                        return wifi.radio.connected

                if not wifi.radio.connected and self.wifi_never_connected:
                        try:
                                # Reconnections happen automatically once one connection is successful
                                wifi.radio.connect(self.wifi_ssid, self.wifi_password)
                                print('✅ Connected to %s' % self.wifi_ssid)
                                print('   bssid=%s' % [hex(i) for i in wifi.radio.ap_info.bssid])
                                print('   rssi=%d' % wifi.radio.ap_info.rssi)
                                print('   channel=%d' % wifi.radio.ap_info.channel)
                                print('   country=%s' % wifi.radio.ap_info.country)
                                print('   authmode=%s' % wifi.radio.ap_info.authmode)
                                print('   mac=%s' % [hex(i) for i in wifi.radio.mac_address])
                                self.wifi_never_connected = False
				self.socket_pool = socketpool.SocketPool(wifi.radio)
                                time.sleep(1)   # Wait for WiFi to come online
                        except OSError as e:
                                print(f"❌ Wifi failed to connect due to OSError: {e}")

                self.wifi_last_connection_attempt = time.monotonic()

		if wifi.radio.connected:
			self.wifi_connect_socket()

                return wifi.radio.connected


	def wifi_connect_socket(self):
		try:
			print('Creating socket...')
			self.socket = self.socket_pool.socket(self.socket_pool.AF_INET, self.socket_pool.SOCK_STREAM)
			self.socket.settimeout(self.SOCKET_TIMEOUT)

			print('Connecting...')
			self.socket.connect((self.ip_addr, self.port))
			print('Socket connected')
		except BaseException as e:
			print('failed to create socket: %s' % e)
			if self.socket is not None:
				self.socket.close()
			self.socket = None


	def connect_st4(self):
		pass


	def connect(self):
		if self.con_type == 'wifi':
			self.connect_wifi();
		elif self.con_type == 'st4':
			self.connect_st4()


	def send_command(self, cmd, reply_expected = True):
		"""
			All mount operations start with a send command and receive a reply. Commands should not include the starting : or ending #
			Some commands don't expect a reply, in which case set reply_expected to False
	
			Returns a Tuple: (success, response)
				success: True for success, false for error
				response: The response, or None in case of error of no response (some commands don't expect a response)
		"""

		if not self.connected():
			print('Error: Network or socket not connected')
			return (False, None)

		cmd = ':' + cmd + '#'		# Prepend : and append #
		if self.debug:
			print('tx: %s -> ' % cmd, end='')

   

		# Send the command
		if self.con_type == 'wifi':
			try:
				bytesSent = self.socket.send(cmd)
				if bytesSent != len(cmd):
					raise ValueError('send_command: %d != %d' % (bytesSent, len(cmd)))
			except:
				print('Error: Network or socket not connected')
				if self.socket is not None:
					self.socket.close()
				self.socket = None
				return (False, None)

		elif self.con_type == 'st4':
			pass

		# Receive the response if we expect to get one
		if reply_expected:
			if self.con_type == 'wifi':
				rxBuf = bytearray(self.MAX_RX_SIZE)
				try:
					rxBytes = self.socket.recv_into(rxBuf)
				except:
					print('Error: Network or socket not connected')
					if self.socket is not None:
						self.socket.close()
					self.socket = None
					return (False, None)

				rxBuf = rxBuf[0:rxBytes].decode()
				if len(rxBuf) == 0:
					raise ValueError('send_command: received zero bytes')
			elif self.con_type == 'st4':
				pass
		else:
			rxBuf = None

		if self.debug:
			print('rx: %s' % rxBuf)

		# Any reply can be :data#, 0 (fail) or 1 (success), let's figure it out
		if rxBuf is None:
			if reply_expected:
				raise ValueError('send_command: expected a response but didn\'t get one')
		else:
			if rxBuf == '0':
				return (False, None)
			elif rxBuf == '1':
				return (True, None)
			elif rxBuf[-1] == '#':
				return (True, rxBuf[:-1])
			else:
				raise ValueError('send_command: unrecognized response: %s' % rxBuf)

		# Shouldn't reach here
		return None
