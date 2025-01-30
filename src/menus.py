"""

WCO Catalog:
For common targets we really hit the most common Messiers objects and planets and the moon most often. For Messier objects, probably M3, M4, M8, M11, M13, M15, M16, M17, M27, M31, M42, M44, M45, M46, M51, M53, M57, M63, M65, M66, M81, M82, M84, M86, M92, M97, M101, M104, M106. Oooof that might have been more than you were thinking of adding. 😅 feel free to pick your favourites and exclude the rest!
Top 10 would be: 3,11,13,16,27,42,53,57,81,92


If mode == MODE_DATETIME_REQUIRED:
	display prompt "Enter date time"
elif mode == MODE_UNPARK_NEEDED:
	display prompt "Press ENTER to unpark"
elif mode == MODE_HOME_NEEDED:
	display prompt "Slew to DEC 90 with forks East/West and press ENTER when ready"
else:
	Display normal menus


menuItemSubmenu(name, submenu)
menuItemAction(name, op)
menuItemView(name, value)

	self.menu = [
			menuItemSubmenu('OBJECT LIBRARY', self.menu_objectlibrary)
			menuItemSubmenu('TARGET', self.menu_target)
			menuItemSubmenu('SYNC TARGET', self.menu_synctarget)
			menuItemSubmenu('PARK', self.menu_park)
			menuItemSubmenu('HOME', self.menu_home)
			menuItemSubmenu('SPIRAL SEARCH', self.menu_spiralsearch)
			menuItemSubmenu('TRACKING', self.menu_tracking)
			menuItemSubmenu('ALIGN', self.menu_align)
			menuItemSubmenu('POSITION', self.menu_position)
			menuItemSubmenu('DATE/TIME', self.menu_datetime)
			menuItemSubmenu('MAP LIGHT', self.menu_maplight)
			menuItemSubmenu('ABOUT', self.menu_about)
		    ]

	self.menu_objectlibrary =  [
			menuItemSubmenu('Solar System', self.menu_object_library_catSolarSystem)
			menuItemSubmenu('NGC', self.menu_object_library_catNgc)
			menuItemSubmenu('IC', self.menu_object_library_catIc)
			menuItemSubmenu('Messier', self.menu_object_library_catMessier)
		]

	self.menu_target = [
			menuItemView('Target RA', self.view_targetRa
		]

	MENUS = [
		{'name': 'OBJECT LIBRARY', 'view': self.view_object_library, 'menu': None,},	# View object library
		{'name': 'TARGET', 'view': self.view_target, 'menu': None,},	# View object library
	]


TARGET
	TARGET RA:
	TARGET DEC:
	SET NEW TARGET
		ENTER RA/DEC

SYNC TARGET:
	Press ENTER to Sync current position with target

PARK
	PARK SCOPE
	SET PARK POSITION (may not be needed)

HOME
	GO HOME
	SET HOME

SPIRAL SEARCH
	Press ENTER to start spiral search, press ENTER again to stop

TRACKING
	SWITCH ON (or SWITCH OFF depending on state)
	RATE: SIDEREAL
	RATE: LUNAR
	RATE: SOLAR
	REFRACTION COMP: SWITCH ON  (or SWITCH Off depending on state)

ALIGN
	ALIGN 1-STAR
	ALIGN 2-STAR

POSITION
	RA: 00o 11' 12"
	DEC: +-00o 11' 12"
	AZ: 000o 11' 12"
	ALT: 00o 11' 12"

		
DATE/TIME
	DATE: 07/11/91
	TIME: 00:23:23
	LTST: 21:38:02

MAP LIGHT
	SWITCH ON (or switch off depending on mode)

ABOUT
	PiHC Version: 1.0.0a
	OnStepX Version: 13.2
	Info: SkyPilot - Wilson Coulee
	Author: @ChasinSpin


Joystick:
	Center button switches between Joystick and Non-Joystick mode
	In Joystick mode, N/S/W/E slew and Center button stops and F1/F2 decrease/increase slew speed
	In Non-Joystick mode, N/S/W/E navigate the menu

	It starts up in non-joystick mode.

	When not in a mode that's an input field:

		N/S/W/E and Center(Stop) 


Status display at top:

Mode: Menu or Slew
SlewSpeed Error Tracking etc.

Target:
	M57 EX PNEB
	MAG 9.7 SZ 2.5'


"""


import time
from connectionManager import ConnectionManager



class menuItemSubmenu():

	def __init__(self, name, submenu):
		self.name = name
		self.submenu = submenu



class menuItemAction():

	def __init__(self, name, operation, arg = None):
		self.name = name
		self.operation = operation
		self.arg = arg


class menuItemView():

	def __init__(self, name, value):
		self.name = name
		self.value = value


class menu():

	MAX_MENU_LINES = 3
	
	def __init__(self, menu):
		self.menu		= menu
		self.selected_index 	= 0
		self.selected_lower	= 0
		self.selected_upper	= min(len(self.menu), self.MAX_MENU_LINES)


class Menus():

	MODE_DISPLAY_OPERATION		= 0	# Displays an operation; PARKED, PARK_INPROGRESS, GOTO_INPROGRESS, ERROR
	MODE_MENU			= 1	# Displays the menu
	MODE_JOYSTICK			= 2	# Displays the joystick
	MODE_VIEW			= 3	# Displays a view after an action

	DISPLAY_OP_NONE			= 0
	DISPLAY_OP_PARKED		= 1
	DISPLAY_OP_PARK_INPROGRESS	= 2
	DISPLAY_OP_GOTO_INPROGRESS	= 3
	DISPLAY_OP_3STARALIGN		= 4
	DISPLAY_OP_ERROR		= 5

	STATUS_TIMEOUT			= 1.0
	JOYSTICK_RETRANSMIT_TIMEOUT	= 5.0
	


	def __init__(self, connection_manager, pyhc_version, info):
		self.mode		= self.MODE_MENU
		self.display_op		= self.DISPLAY_OP_NONE
		self.menu_updated	= False
		self.joystick_mode	= False
		self.guide_rate		= 9
		self.conman		= connection_manager
		self.pyhc_version	= pyhc_version
		self.info		= info

		self.menu_parking = [
			menuItemAction('PARK', self.action_park),
			menuItemAction('UNPARK', self.action_unpark),
		]

		#self.menu_home = [
		#	menuItemAction('MOVE HOME', self.action_movehome),
		#	menuItemAction('SET HOME', self.action_sethome),
		#]

		self.menu_tracking = [
			menuItemAction('TRACKING ON', self.action_trackingon),
			menuItemAction('TRACKING OFF', self.action_trackingoff),
		]

		self.menu_trackingrate = [
			menuItemAction('SIDEREAL', self.action_trackingrate, 'sidereal'),
			menuItemAction('LUNAR', self.action_trackingrate, 'lunar'),
			menuItemAction('KING', self.action_trackingrate, 'king'),
			menuItemAction('SOLAR', self.action_trackingrate, 'solar'),
		]

		self.menu_maxslewrate = [
			menuItemAction('NORMAL (4 deg/s)', self.action_maxslewrate, 'normal'),
			menuItemAction('COLD WEATHER (2.7 deg/s)', self.action_maxslewrate, 'coldweather'),
			menuItemAction('SNAIL PACE (2.0 deg/s)', self.action_maxslewrate, 'snailpace'),
			menuItemAction('INSANE (6.0 deg/s)', self.action_maxslewrate, 'insane'),
		]

		self.menu_admin = [
			menuItemAction('SETPARK (do not use)', self.action_setpark),
		]

		self.main_menu = [
			menuItemSubmenu('PARKING', self.menu_parking),
			menuItemAction('SYNC', self.action_sync),
			menuItemView('POSITION', self.view_position),
			menuItemSubmenu('TRACKING ON/OFF', self.menu_tracking),
			menuItemSubmenu('TRACKING RATE', self.menu_trackingrate),
			menuItemSubmenu('MAX SLEW RATE', self.menu_maxslewrate),
			menuItemAction('3 STAR ALIGN', self.action_3staralign),
			menuItemAction('ABOUT', self.action_about),
			menuItemSubmenu('ADMIN ONLY', self.menu_admin),
		]

		self.menu_stack			= []
		self.current_menu		= menu(self.main_menu)

		self.last_get_status		= time.monotonic()
		self.last_status = {}
		self.last_3staralign_time	= time.monotonic()



	def __get_status(self):
		now = time.monotonic()

		if now >= self.last_get_status + self.STATUS_TIMEOUT:
			self.last_get_status = now
			rx = self.conman.send_command('GU', reply_expected = True)	# Status
			self.status =  {}

			if rx is None:
				return

			if 'P' in rx:
				self.status['parked'] = 'yes'
			elif 'p' in rx:
				self.status['parked'] = 'no'
			elif 'F' in rx:
				self.status['parked'] = 'fail'
			elif 'I' in rx:
				self.status['parked'] = 'inprogress'

			if 'H' in rx:
				self.status['athome'] = 'yes'
			elif 'h' in rx:
				self.status['athome'] = 'inprogress'
			else:
				self.status['athome'] = 'no'

			if 'B' in rx:
				self.status['autohomeatboot'] = 'yes'
			else:
				self.status['autohomeatboot'] = 'no'

			if 'n' in rx:
				self.status['tracking'] = 'no'
			else:
				self.status['tracking'] = 'yes'

			if 'R' in rx:
				self.status['pec'] = 'recorded'
			else:
				self.status['pec'] = 'notrecorded'

			if 'G' in rx:
				self.status['pulseguiding'] = 'yes'
			else:
				self.status['pulseguiding'] = 'no'

			if 'g' in rx:
				self.status['guiding'] = 'yes'
			else:
				self.status['guiding'] = 'no'

			if 'S' in rx:
				self.status['pps'] = 'yes'
			else:
				self.status['pps'] = 'no'

			if 'N' in rx:
				self.status['goto'] = 'no'
			else:
				self.status['goto'] = 'yes'

			if 'e' in rx:
				self.status['synctoencoders'] = 'yes'
			else:
				self.status['synctoencoders'] = 'no'

			if 'rs' in rx:
				self.status['refraction'] = 'refraction,enabled,singleaxis'
			elif 'r' in rx:
				self.status['refraction'] = 'enabled'
			elif 'ts' in rx:
				self.status['refraction'] = 'ontrack,enabled,singleaxis'
			elif 't' in rx:
				self.status['refraction'] = 'ontrack,enabled'
			else:
				self.status['refraction'] = 'disabled'

			if '(' in rx:
				self.status['trackingrate'] = 'lunar'
			elif 'O' in rx:
				self.status['trackingrate'] = 'solar'
			elif 'k' in rx:
				self.status['trackingrate'] = 'king'
			else:
				self.status['trackingrate'] = 'sidereal'

			if 'w' in rx:
				self.status['waitingathome'] = 'yes'
			else:
				self.status['waitingathome'] = 'no'

			if 'u' in rx:
				self.status['pauseathomeenabled'] = 'yes'
			else:
				self.status['pauseathomeenabled'] = 'no'

			if 'z' in rx:
				self.status['buzzer'] = 'yes'
			else:
				self.status['buzzer'] = 'no'

			if 'a' in rx:
				self.status['automeridianflip'] = 'yes'
			else:
				self.status['automeridianflip'] = 'no'

			if '/' in rx:
				self.status['pecstate'] = 'ignore,ready'
			elif ',' in rx:
				self.status['pecstate'] = 'lay'
			elif '~' in rx:
				self.status['pecstate'] = 'laying, ready'
			elif ';' in rx:
				self.status['pecstate'] = 'record'
			elif '^' in rx:
				self.status['pecstate'] = 'recording'

			if 'E' in rx:
				self.status['mounttype'] = 'gem'
			elif 'K' in rx:
				self.status['mounttype'] = 'fork'
			elif 'A' in rx:
				self.status['mounttype'] = 'altazm'
			elif 'L' in rx:
				self.status['mounttype'] = 'altalt'

			if 'o' in rx:
				self.status['pierside'] = 'none'
			elif 'T' in rx:
				self.status['pierside'] = 'east'
			elif 'W' in rx:
				self.status['pierside'] = 'west'

			if '0' in rx:
				rx2 = rx.lstrip('0')
				rx2 = rx2[0:2]
				self.status['error'] = rx2	# This can be pulse rate, guide rate or error code, not sure

			if self.last_status != self.status:
				self.menu_updated = True
				self.last_status = self.status
				print(self.status)


	def __get_status_shortform(self):
		str = 'Park:'
		if self.status['parked'] == 'yes':
			str += 'Y'
		elif self.status['parked'] == 'no':
			str += 'N'
		elif self.status['parked'] == 'failed':
			str += 'F'
		elif self.status['parked'] == 'inprogress':
			str += 'i'

		str += ' Trk:'
		if self.status['tracking'] == 'yes':
			if self.status['trackingrate'] == 'lunar':
				str +=  'lun'
			elif self.status['trackingrate'] == 'solar':
				str +=  'sol'
			elif self.status['trackingrate'] == 'king':
				str +=  'kg'
			else:
				str +=  'sid'
		elif self.status['tracking'] == 'no':
			str += 'off'

		str += ' GPS: '
		if self.status['pps'] == 'yes':
			str += 'Y'
		elif self.status['pps'] == 'no':
			str += 'N'

		str += ' err:'
		#str += self.status['error']

		return str


	def __check_display_op(self):
		if self.menu_updated:
			#if 'error' in self.last_status.keys():
			#	# Error is always checked for first
			#	self.mode	= self.MODE_DISPLAY_OPERATION
			#	self.display_op	= self.DISPLAY_OP_ERROR
			#	print('ERROR')
			#	print(self.last_status['error'])
			if self.last_status['parked'] == 'yes':
				self.mode	= self.MODE_DISPLAY_OPERATION
				self.display_op	= self.DISPLAY_OP_PARKED
			elif self.last_status['parked'] == 'inprogress':
				self.mode	= self.MODE_DISPLAY_OPERATION
				self.display_op	= self.DISPLAY_OP_PARK_INPROGRESS
			elif self.display_op != self.DISPLAY_OP_3STARALIGN and self.last_status['goto'] == 'yes':
				self.mode	= self.MODE_DISPLAY_OPERATION
				self.display_op	= self.DISPLAY_OP_GOTO_INPROGRESS
			elif self.display_op == self.DISPLAY_OP_3STARALIGN:
				pass
			else:
				self.mode = self.MODE_MENU
				self.display_op = self.DISPLAY_OP_NONE

		if self.mode == self.MODE_DISPLAY_OPERATION and self.display_op == self.DISPLAY_OP_3STARALIGN:
			now = time.monotonic()
			if (now - self.last_3staralign_time) >= 1:
				self.last_3staralign_time = now
				self.menu_updated = True
        

	def needs_redisplay(self):
		""" Returns true if the menu has been updated and needs display """
		self.__get_status()
		self.__check_display_op()

		return self.menu_updated


	def get_menu_display(self):
		""" Returns the current menu we need to display """
		self.menu_updated = False

		lines = []

		if self.mode == self.MODE_DISPLAY_OPERATION and self.display_op == self.DISPLAY_OP_3STARALIGN:
                	rx = self.conman.send_command('A?', reply_expected = True)
			starNum = rx[1]
			if starNum == '4':
                		self.conman.send_command('AW', reply_expected = True)
				self.mode = self.MODE_MENU
				self.display_op = self.DISPLAY_OP_NONE
			else:
				lines = ['Align Star %s' % starNum, 'Select star in SkySafari', 'away from NCP and', 'goto and Align']

		print('Mode:', self.mode)
		print('Display Op:', self.display_op)
		if self.mode == self.MODE_VIEW or self.mode == self.MODE_JOYSTICK:
			lines = self.view_msg
		elif self.mode == self.MODE_DISPLAY_OPERATION:
			if   self.display_op == self.DISPLAY_OP_PARKED:
				lines = ['MOUNT IS PARKED!', '', 'Press W button', 'to unpark']
			elif self.display_op == self.DISPLAY_OP_PARK_INPROGRESS:
				lines = ['MOVING MOUNT TO PARK POSITION!', '', 'Press ANY button', 'to STOP']
			elif self.display_op == self.DISPLAY_OP_GOTO_INPROGRESS:
				lines = ['MOVING MOUNT TO TARGET POSITION!', '', 'Press ANY button', 'to STOP']
			elif self.display_op == self.DISPLAY_OP_ERROR:
				lines = ['ERROR']
			#elif self.display_op == self.DISPLAY_OP_NONE:
			#	self.mode = self.MODE_MENU
		else:
			lines.append(self.__get_status_shortform())

			for i in range(self.current_menu.selected_lower, self.current_menu.selected_upper):
				if i == self.current_menu.selected_index:
					cursor = '> '
				else:
					cursor = '  '
				lines.append('%s%s' % (cursor, self.current_menu.menu[i].name))

		return lines


	def __process_buttons_joystick(self, buttonsPressed, buttonsReleased, buttonsHeld):

		now = time.monotonic()

		if self.last_joystick_tx + self.JOYSTICK_RETRANSMIT_TIMEOUT <= now:
			retransmit_timeout = True
			self.last_joystick_tx = now
		else:
			retransmit_timeout = False

		if 'F1' in buttonsPressed:
			""" Decrease slew speed """
			self.guide_rate -= 1
			if self.guide_rate < 0:
				self.guide_rate = 0
                	self.conman.send_command('R%d' % self.guide_rate, reply_expected = False)      # Set guide rate
			self.__setJoystickView()

		if 'F2' in buttonsPressed:
			""" Increase slew speed """
			self.guide_rate += 1
			if self.guide_rate > 9:
				self.guide_rate = 9
                	self.conman.send_command('R%d' % self.guide_rate, reply_expected = False)      # Set guide rate
			self.__setJoystickView()
		

		if 'N' in buttonsPressed or ('N' in buttonsHeld and retransmit_timeout):
			self.conman.send_command('Mn', reply_expected = False)
		if 'S' in buttonsPressed or ('S' in buttonsHeld and retransmit_timeout):
			self.conman.send_command('Ms', reply_expected = False)
		if 'E' in buttonsPressed or ('E' in buttonsHeld and retransmit_timeout):
			self.conman.send_command('Me', reply_expected = False)
		if 'W' in buttonsPressed or ('W' in buttonsHeld and retransmit_timeout):
			self.conman.send_command('Mw', reply_expected = False)

		if 'N' in buttonsReleased:
			self.conman.send_command('Qn', reply_expected = False)
		if 'S' in buttonsReleased:
			self.conman.send_command('Qs', reply_expected = False)
		if 'E' in buttonsReleased:
			self.conman.send_command('Qe', reply_expected = False)
		if 'W' in buttonsReleased:
			self.conman.send_command('Qw', reply_expected = False)


	def __setJoystickView(self):
		rates = ['0.25X', '0.5X', '1X', '2X', '4X', '8X', '20X', '48X', '1/2Max', 'Max']
		self.set_joystick_view( [ 'Joystick Mode', 'Rate: %s' % rates[self.guide_rate] ] )
			

	def process_buttons(self, buttonsPressed, buttonsReleased, buttonsHeld):
		""" Process button inputs and change menus accordingly """

		if 'C' in buttonsPressed:
			if self.mode == self.MODE_JOYSTICK:
				self.mode = self.MODE_MENU
				self.conman.send_command('Q', reply_expected = False)
				print('QUIT JOYSTICK MODE')
			else:
				self.__setJoystickView()
				print('JOYSTICK MODE')
				self.mode = self.MODE_JOYSTICK
				self.last_joystick_tx = time.monotonic()
                		self.conman.send_command('R%d' % self.guide_rate, reply_expected = False)      # Set guide rate

		if self.mode == self.MODE_JOYSTICK:
			self.__process_buttons_joystick(buttonsPressed, buttonsReleased, buttonsHeld)
		else:
			if len(buttonsPressed) == 0:
				return

			if self.display_op == self.DISPLAY_OP_PARK_INPROGRESS or self.display_op == self.DISPLAY_OP_GOTO_INPROGRESS:
                		self.conman.send_command('Q', reply_expected = False)	# Stop motion
				
			if self.mode == self.MODE_VIEW:
				self.mode = self.MODE_MENU
			if self.mode == self.MODE_DISPLAY_OPERATION:
				if   self.display_op == self.DISPLAY_OP_PARKED:
					if 'W' in buttonsPressed:
						self.action_unpark()
				elif   self.display_op == self.DISPLAY_OP_NONE:
					self.mode = self.MODE_MENU
			else:
				if 'S' in buttonsPressed:
					self.current_menu.selected_index += 1
					if self.current_menu.selected_index >= len(self.current_menu.menu):
						self.current_menu.selected_index = len(self.current_menu.menu) - 1
					elif self.current_menu.selected_index >= self.current_menu.selected_upper:
						self.current_menu.selected_upper += 1
						self.current_menu.selected_lower += 1
	
				if 'N' in buttonsPressed:
					self.current_menu.selected_index -= 1
					if self.current_menu.selected_index < 0:
						self.current_menu.selected_index = 0
					elif self.current_menu.selected_index < self.current_menu.selected_lower:
						self.current_menu.selected_lower -= 1
						self.current_menu.selected_upper -= 1
		
				if 'E' in buttonsPressed:
					if len(self.menu_stack):
						self.menu_stack.pop()
						if len(self.menu_stack):
							self.current_menu = self.menu_stack[-1]
						else:
							self.current_menu		= menu(self.main_menu)
				
	
				if 'W' in buttonsPressed:
					selected = self.current_menu.menu[self.current_menu.selected_index]
					if isinstance(selected, menuItemSubmenu):
						self.menu_stack.append(self.current_menu)
						self.current_menu = menu(selected.submenu)
					if isinstance(selected, menuItemAction):
						if selected.arg is not None:
							selected.operation(selected.arg)
						else:
							selected.operation()
					if isinstance(selected, menuItemView):
						pass

		self.menu_updated = True


	def set_view(self, msg):
		self.mode		= self.MODE_VIEW
		self.view_msg		= msg
		self.menu_updated	= True


	def set_joystick_view(self, msg):
		self.view_msg		= msg
		self.menu_updated	= True


	def action_park(self):
		self.conman.send_command('hP', reply_expected = True)
		self.set_view(['Mount is now PARKED!'])
		print('PARKED')


	def action_unpark(self):
		self.conman.send_command('hR', reply_expected = True)
		self.conman.send_command('RG', reply_expected = False)
		self.conman.send_command('R9', reply_expected = False)
		self.set_view(['Mount is now UNPARKED', 'and Rates Set To Fast!'])
		print('UNPARKED')


	def action_setpark(self):
		self.conman.send_command('hQ', reply_expected = True)
		self.set_view(['Mount has had it\'s park position SET'])
		print('SET PARK')


	def action_movehome(self):
		self.conman.send_command('hC', reply_expected = False)
		self.set_view(['Mount is moving (finding) HOME'])
		print('MOVE HOME')


	def action_sethome(self):
		self.conman.send_command('hF', reply_expected = False)
		self.set_view(['Mount has had it\'s home position SET'])
		print('SET HOME')


	def action_trackingon(self):
		self.conman.send_command('Te', reply_expected = True)
		self.set_view(['Mount has tracking ENABLED'])
		print('TRACKING ON')


	def action_trackingoff(self):
		self.conman.send_command('Td', reply_expected = True)
		self.set_view(['Mount has tracking DISABLED'])
		print('TRACKING OFF')


	def action_sync(self):
		self.conman.send_command('CS', reply_expected = False)	# This maybe CM, not sure
		self.set_view(['Synced current position to target!'])
		print('SYNC')


	def action_about(self):
		onstepx_ver = self.conman.send_command('GVN', reply_expected = True)
		self.set_view( ['PiHC Version: %s' % self.pyhc_version, 'OnStepX Version: %s' % onstepx_ver, 'Info: %s' % self.info, 'Author: @ChasinSpin'] )
		print('ABOUT')


	def action_maxslewrate(self, arg):
		if arg == 'coldweather':
			speed = 4
		elif arg == 'snailpace':
			speed = 5
		elif arg == 'insane':
			speed = 2
		else:
			speed = 3

		self.conman.send_command('SX93,%d' % speed, reply_expected = False)
		self.set_view(['Max slew speed set'])


	def action_trackingrate(self, arg):
		if arg == 'sidereal':
			self.conman.send_command('TQ', reply_expected = False)
		elif arg == 'solar':
			self.conman.send_command('TS', reply_expected = False)
		elif arg == 'lunar':
			self.conman.send_command('TL', reply_expected = False)
		elif arg == 'king':
			self.conman.send_command('TK', reply_expected = False)
		self.set_view(['Tracking rate set'])


	def action_3staralign(self):
		self.mode = self.MODE_DISPLAY_OPERATION
		self.display_op = self.DISPLAY_OP_3STARALIGN
		self.conman.send_command('A3', reply_expected = True)

	
	def view_position(self)
		ra = send_command('GR', reply_expected = True)
		dec = send_command('GD', reply_expected = True)
		az = send_command('GZ', reply_expected = True)
		alt = send_command('GA', reply_expected = True)
		display.display_position(ra, dec, az, alt)


	def view_position(self):
		pass
