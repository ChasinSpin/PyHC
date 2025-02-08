"""

WCO Catalog:
For common targets we really hit the most common Messiers objects and planets and the moon most often. For Messier objects, probably M3, M4, M8, M11, M13, M15, M16, M17, M27, M31, M42, M44, M45, M46, M51, M53, M57, M63, M65, M66, M81, M82, M84, M86, M92, M97, M101, M104, M106. Oooof that might have been more than you were thinking of adding. 😅 feel free to pick your favourites and exclude the rest!
Top 10 would be: 3,11,13,16,27,42,53,57,81,92


	self.menu = [
			menuItemSubmenu('OBJECT LIBRARY', self.menu_objectlibrary)
		    ]

	self.menu_objectlibrary =  [
			menuItemSubmenu('Solar System', self.menu_object_library_catSolarSystem)
			menuItemSubmenu('NGC', self.menu_object_library_catNgc)
			menuItemSubmenu('IC', self.menu_object_library_catIc)
			menuItemSubmenu('Messier', self.menu_object_library_catMessier)
		]

	MENUS = [
		{'name': 'OBJECT LIBRARY', 'view': self.view_object_library, 'menu': None,},	# View object library
	]

Target:
	M57 EX PNEB
	MAG 9.7 SZ 2.5'

  #include "src/catalogs/data/stars.h"           // Catalog of 408 bright stars
  #include "src/catalogs/data/messier.h"         // Charles Messier's famous catalog of 109 DSO's
  #include "src/catalogs/data/caldwell.h"        // The Caldwell (supplement) catalog of 109 DSO's
  #include "src/catalogs/data/ngc.h"             // The New General Catalog of 8154 DSO's
  #include "src/catalogs/data/ic.h"              // The Index Catalog (supplement) of 5400 DSO's



"""


import time
import board
import neopixel
from connectionManager import ConnectionManager
from adafruit_datetime import datetime, timedelta



class menuItemSubmenu():

	def __init__(self, name, submenu, site_manager_only):
		self.name = name
		self.submenu = submenu
		self.site_manager_only = site_manager_only



class menuItemAction():

	def __init__(self, name, confirmation, operation, arg = None):
		self.name = name
		self.confirmation = confirmation
		self.operation = operation
		self.arg = arg


class menuItemView():

	def __init__(self, name, view, arg, update_rate = None):
		self.name = name
		self.view = view
		self.arg = arg
		self.update_rate = update_rate


class menu():

	MAX_MENU_LINES = 3
	
	def __init__(self, menu):
		self.menu		= menu
		self.selected_index 	= 0
		self.selected_lower	= 0
		self.selected_upper	= min(len(self.menu), self.MAX_MENU_LINES)

	def __str__(self):
		return 'menu: selected_index:%d selected_lower:%d selected_upper:%d' % (self.selected_index, self.selected_lower, self.selected_upper)


class Menus():

	MODE_NORMAL			= 0	# Normal mode, displays menu or other information
	MODE_JOYSTICK			= 1	# Takes joystick input

	STATUS_TIMEOUT			= 1.0
	JOYSTICK_RETRANSMIT_TIMEOUT	= 5.0
	


	def __init__(self, connection_manager, pyhc_version, info):
		self.mode		= self.MODE_NORMAL
		self.needs_display	= True
		self.status_changed	= True
		self.joystick_mode	= False
		self.guide_rate		= 9
		self.conman		= connection_manager
		self.pyhc_version	= pyhc_version
		self.info		= info

		self.menu_parking = [
			menuItemAction('PARK', None, self.action_park),
			menuItemAction('UNPARK', ['UNPARK command sent'], self.action_unpark),
		]

		self.menu_tracking = [
			menuItemAction('TRACKING ON', ['TRACKING switched ON', '', 'Press any button to continue'], self.action_trackingon),
			menuItemAction('TRACKING OFF', ['TRACKING switched OFF', '', 'Press any button to continue'], self.action_trackingoff),
		]

		self.menu_trackingrate = [
			menuItemAction('SIDEREAL', ['TRACKING set to SIDEREAL', '', 'Press any button to continue'], self.action_trackingrate, 'sidereal'),
			menuItemAction('LUNAR', ['TRACKING set to LUNAR', '', 'Press any button to continue'], self.action_trackingrate, 'lunar'),
			menuItemAction('KING', ['TRACKING set to KING', '', 'Press any button to continue'], self.action_trackingrate, 'king'),
			menuItemAction('SOLAR', ['TRACKING set to SOLAR', '', 'Press any button to continue'], self.action_trackingrate, 'solar'),
		]

		self.menu_maxslewrate = [
			menuItemAction('NORMAL (4 deg/s)', ['MAX SLEW RATE set to', 'NORMAL(4 deg/s)', '', 'Press any button to continue'], self.action_maxslewrate, 'normal'),
			menuItemAction('COLD WEATHER (2.7 deg/s)', ['MAX SLEW RATE set to', 'COLD WEATHER (2.7 deg/s)', '', 'Press any button to continue'], self.action_maxslewrate, 'coldweather'),
			menuItemAction('SNAIL PACE (2.0 deg/s)', ['MAX SLEW RATE set to', 'SNAIL PACE (2.0 deg/s)', '', 'Press any button to continue'], self.action_maxslewrate, 'snailpace'),
			menuItemAction('INSANE (6.0 deg/s)', ['MAX SLEW RATE set to', 'INSANE (6.0 deg/s)', '', 'Press any button to continue'], self.action_maxslewrate, 'insane'),
		]

		self.menu_maplight = [
			menuItemAction('MAP LIGHT ON', ['MAP LIGHT switched ON', '', 'Press any button to continue'], self.action_maplighton),
			menuItemAction('MAP LIGHT OFF', ['MAP LIGHT switched OFF', '', 'Press any button to continue'], self.action_maplightoff),
		]

		self.menu_admin = [
			menuItemAction('SETPARK', ['CURRENT POSITION IS', 'NOW THE PARK POSITION!', '', 'Press any button to continue'], self.action_setpark),
			menuItemAction('3 STAR ALIGN', None, self.action_3staralign),
		]

		self.main_menu = [
			menuItemSubmenu('PARKING', self.menu_parking, False),
			menuItemAction('SYNC (ALIGN)', ['CURRENT POSITION aligned', 'to CURRENT TARGET', '', 'Press any button to continue'], self.action_sync),
			menuItemAction('SPIRAL SEARCH', None, self.action_spiral_search),
			menuItemView('POSITION', self.view_position, None, 1),
			menuItemSubmenu('TRACKING ON/OFF', self.menu_tracking, False),
			menuItemSubmenu('TRACKING RATE', self.menu_trackingrate, False),
			menuItemSubmenu('MAX SLEW RATE', self.menu_maxslewrate, False),
			menuItemSubmenu('MAP LIGHT', self.menu_maplight, False),
			menuItemView('DATE/TIME', self.view_date_time, None, 1),
			menuItemView('SITE', self.view_site, None, None),
		
			menuItemView('ABOUT', self.view_about, None, None),
			menuItemSubmenu('SITE MANAGER ONLY', self.menu_admin, True),
		]

		self.menu_stack			= []
		self.top_level_menu		= menu(self.main_menu)
		self.current_menu		= self.top_level_menu

		self.last_get_status		= time.monotonic()
		self.last_status = {}
		self.last_3staralign_time	= time.monotonic()
		self.last_active_view_update	= time.monotonic()

		self.periodic_menu_update	= time.monotonic()

		self.display_lines		= []
		self.active_view		= None
		self.active_view_terminate	= None

		self.pixel			= neopixel.NeoPixel(board.NEOPIXEL, 1)

		self.last_joystick_tx		= time.monotonic()


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
	
			self.status['guideratepulse'] = ord(rx[-3]) - ord('0')
			self.status['guiderate'] = ord(rx[-2]) - ord('0')

			errStrs = [
				None,
				'Motor/driver fault',
				'Below horizon limit', 
				'Limit sense',
				'Dec limit exceeded',
				'Azm limit exceeded',
				'Under pole limit exceeded',
				'Meridian limit exceeded',
				'Sync safety limit exceeded',
				'Park failed',
				'Goto sync failed',
				'Unknown error',
				'Above overhead limit',
				'Weather sensor init failed',
				'Time or loc. not updated',
				'Init NV/EEPROM error',
				'Unknown Error, code: ',
			]

			errCode = ord(rx[-1]) - ord('0')
			self.status['error'] = errCode

			if errCode < 0 or errCode >= len(errStrs):
				self.status['errorStr'] = errStrs[-1] + str(errCode)
			else:
				self.status['errorStr'] = errStrs[errCode]

			if self.last_status != self.status:
				self.status_changed = True
				self.last_status = self.status
				print(self.status)
			else:
				self.status_changed = False


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

		str += ' GPS:'
		if self.status['pps'] == 'yes':
			str += 'Y'
		elif self.status['pps'] == 'no':
			str += 'N'

		str += ' err:'
		if self.status['error'] == 0:
			str += 'N'
		else:
			str += self.status['error']

		return str


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
			self.active_view(self.active_view_arg)
			self.needs_display = True

		if 'F2' in buttonsPressed:
			""" Increase slew speed """
			self.guide_rate += 1
			if self.guide_rate > 9:
				self.guide_rate = 9
                	self.conman.send_command('R%d' % self.guide_rate, reply_expected = False)      # Set guide rate
			self.active_view(self.active_view_arg)
			self.needs_display = True
		

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
			

	def process_menus(self, buttonsPressed, buttonsReleased, buttonsHeld):
		""" Process button inputs and change menus accordingly """
		redisplay_menu = False

		now = time.monotonic()
		if now >= self.periodic_menu_update + 1:
			self.periodic_menu_update = now
			redisplay_menu = True

		if 'S' in buttonsPressed:
			redisplay_menu = True
			self.current_menu.selected_index += 1
			if self.current_menu.selected_index >= len(self.current_menu.menu):
				self.current_menu.selected_index = len(self.current_menu.menu) - 1
			elif self.current_menu.selected_index >= self.current_menu.selected_upper:
				self.current_menu.selected_upper += 1
				self.current_menu.selected_lower += 1

		if 'N' in buttonsPressed:
			redisplay_menu = True
			self.current_menu.selected_index -= 1
			if self.current_menu.selected_index < 0:
				self.current_menu.selected_index = 0
			elif self.current_menu.selected_index < self.current_menu.selected_lower:
				self.current_menu.selected_lower -= 1
				self.current_menu.selected_upper -= 1

		if 'E' in buttonsPressed:
			redisplay_menu = True
			if len(self.menu_stack):
				self.menu_stack.pop()
				if len(self.menu_stack):
					self.current_menu = self.menu_stack[-1]
				else:
					self.current_menu		= self.top_level_menu

		if 'W' in buttonsPressed:
			redisplay_menu = True
			selected = self.current_menu.menu[self.current_menu.selected_index]
			if isinstance(selected, menuItemSubmenu):
				visit_menu = False
				if selected.site_manager_only:
					if 'F1' in buttonsHeld and 'F2' in buttonsHeld:
						visit_menu = True
				else:
					visit_menu = True

				if visit_menu:
					self.menu_stack.append(self.current_menu)
					self.current_menu = menu(selected.submenu)
			if isinstance(selected, menuItemAction):
				selected.operation(selected.arg)
				if selected.confirmation is not None:
					if self.confirmation_view is not None:
						self.active_view = self.confirmation_view
						self.active_view_arg = selected.confirmation
						self.active_view_update_rate = None
						self.active_view_terminate = None
						self.active_view(self.active_view_arg)
				self.needs_display = True
				return
			if isinstance(selected, menuItemView):
				self.active_view = selected.view
				self.active_view_arg = selected.arg
				self.active_view_update_rate = selected.update_rate
				self.active_view_terminate = None
				self.active_view(self.active_view_arg)
				self.needs_display = True
				return


		if redisplay_menu or self.needs_display or self.status_changed:
			self.display_lines = []
			self.display_lines.append(self.__get_status_shortform())

			for i in range(self.current_menu.selected_lower, self.current_menu.selected_upper):
				if i == self.current_menu.selected_index:
					cursor = '> '
				else:
					cursor = '  '
				self.display_lines.append('%s%s' % (cursor, self.current_menu.menu[i].name))

			self.needs_display = True


	def process_status(self, buttonsPressed, buttonsReleased, buttonsHeld):
		used = False

		retButtonsPressed = buttonsPressed

		self.__get_status()

		if self.status is None or self.status == {} or 'error' not in self.status.keys():
			return (used, retButtonsPressed)
	
		if self.status['error'] != 0:
			used = True
			self.display_lines = ['ERROR:', self.status['errorStr'], '', 'Joystick is enabled!']
			self.__process_buttons_joystick(retButtonsPressed, buttonsReleased, buttonsHeld)
			retButtonsPressed = []

		elif self.status['parked'] == 'yes':
			used = True
			self.display_lines = ['MOUNT IS PARKED!', '', 'Press W button to UNPARK']
			if 'W' in buttonsPressed:
				self.action_unpark(None)
				retButtonsPressed = []
				used = False
				self.display_lines = []

		elif self.status['parked'] == 'inprogress':
			used = True
			self.display_lines = ['MOVING MOUNT TO PARK', 'POSITION!', '', 'Press ANY button to STOP']
			if len(retButtonsPressed):
				self.conman.send_command('Q', reply_expected = False)	# Stop motion
				retButtonsPressed = []
				used = False
				self.display_lines = []

		elif self.status['goto'] == 'yes':
			used = True
			self.display_lines = ['MOVING MOUNT TO TARGET', 'POSITION!', '', 'Press ANY button to STOP']
			if len(retButtonsPressed):
				self.conman.send_command('Q', reply_expected = False)	# Stop motion
				retButtonsPressed = []
				used = False
				self.display_lines = []

		if used or self.status_changed:
			self.needs_display = True

		return (used, retButtonsPressed)


	def process_views(self, buttonsPressed, buttonsReleased, buttonsHeld):
		used = False
		clearButtons = False

		if self.active_view is not None:
			used = True

			if self.mode == self.MODE_JOYSTICK:
				self.__process_buttons_joystick(buttonsPressed, buttonsReleased, buttonsHeld)

			elif len(buttonsPressed):
				clearButtons = True
				if self.active_view_terminate is not None:
					self.active_view_terminate()

			if self.active_view_update_rate is not None:
				now = time.monotonic()
				if now >= self.last_active_view_update + self.active_view_update_rate:
					self.active_view(self.active_view_arg)
					self.needs_display = True
					self.last_active_view_update = now
			
		return (used, clearButtons)
		

	def action_park(self, arg):
		self.conman.send_command('hP', reply_expected = True)


	def action_unpark(self, arg):
		self.conman.send_command('Sg+114*01:41', reply_expected = True)	# Set Longitude
		self.conman.send_command('St+50*46:21', reply_expected = True)	# Set Latitude
		self.conman.send_command('SG+07:00', reply_expected = True)	# Set UTC Offset (always this offset, even in daylight savings) - THIS POSSIBLY ISN'T WORKING
		self.conman.send_command('Sh-30', reply_expected = True)	# Set horizon limit
		self.conman.send_command('So90', reply_expected = True)		# Set overhead limit
		self.conman.send_command('hR', reply_expected = True)
		self.conman.send_command('RG', reply_expected = False)
		self.conman.send_command('R9', reply_expected = False)


	def action_setpark(self, arg):
		self.conman.send_command('hQ', reply_expected = True)


	def action_movehome(self, arg):
		self.conman.send_command('hC', reply_expected = False)


	def action_sethome(self, arg):
		self.conman.send_command('hF', reply_expected = False)


	def action_trackingon(self, arg):
		self.conman.send_command('Te', reply_expected = True)


	def action_trackingoff(self, arg):
		self.conman.send_command('Td', reply_expected = True)


	def action_sync(self, arg):
		self.conman.send_command('CS', reply_expected = False)	# This maybe CM, not sure


	def view_about(self, arg):
		onstepx_ver = self.conman.send_command('GVN', reply_expected = True)
		self.display_lines = ['PiHC Version: %s' % self.pyhc_version, 'OnStepX Version: %s' % onstepx_ver, 'Info: %s' % self.info, 'Author: @ChasinSpin']

	
	def view_joystick(self, arg):
		rates = ['0.25X', '0.5X', '1X', '2X', '4X', '8X', '20X', '48X', '1/2Max', 'Max']
		self.display_lines = [ 'Joystick Mode', 'Rate: %s' % rates[self.guide_rate] ]


	def view_date_time(self, arg):
		vDate = self.conman.send_command('GC', reply_expected = True)
		vTime = self.conman.send_command('GL', reply_expected = True)
		vTimeSidereal = self.conman.send_command('GS', reply_expected = True)
		vUtcOffset = self.conman.send_command('GG', reply_expected = True)

		year = int(vDate[6:8]) + 2000
		month = int(vDate[0:2])
		day = int(vDate[3:5])
		hour = int(vTime[0:2])
		min = int(vTime[3:5])
		sec = int(vTime[6:8])

		offset = int(vUtcOffset[0:3]) * 60 * 60 + int(vUtcOffset[4:6]) * 60
		dt = datetime(year, month, day, hour, min, sec)
		delta = timedelta(seconds = offset)
		dt += delta
		self.display_lines = ['UTC: %s' % dt, 'Local Sidereal: %s' % vTimeSidereal, '', 'UTC Offset (inverse): %s' % vUtcOffset]


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


	def action_trackingrate(self, arg):
		if arg == 'sidereal':
			self.conman.send_command('TQ', reply_expected = False)
		elif arg == 'solar':
			self.conman.send_command('TS', reply_expected = False)
		elif arg == 'lunar':
			self.conman.send_command('TL', reply_expected = False)
		elif arg == 'king':
			self.conman.send_command('TK', reply_expected = False)


	def action_3staralign(self, arg):
		self.conman.send_command('A3', reply_expected = True)
		self.active_view = self.view_3staralign
		self.active_view_arg = None
		self.active_view_update_rate = 1
		self.active_view_terminate = None


	def action_spiral_search(self, arg):
		self.conman.send_command('Mp', reply_expected = False)
		self.active_view = self.view_spiral_search
		self.active_view_arg = None
		self.active_view_update_rate = 0.1 
		self.active_view_terminate = self.terminate_spiral_search


	def action_maplighton(self, arg):
		self.pixel.fill( (255, 0, 0) )


	def action_maplightoff(self, arg):
		self.pixel.fill( (0, 0, 0) )

	
	def view_position(self, arg):
		ra = self.conman.send_command('GR', reply_expected = True)
		dec = self.conman.send_command('GD', reply_expected = True)
		az = self.conman.send_command('GZ', reply_expected = True)
		alt = self.conman.send_command('GA', reply_expected = True)
		self.display_lines = ['RA:  %s' % ra, 'DEC: %s' % dec, 'AZ:  %s' % az, 'ALT: %s' % alt]


	def view_3staralign(self, arg):
		rx = self.conman.send_command('A?', reply_expected = True)
		starNum = rx[1]
		if starNum == '4':
			self.conman.send_command('AW', reply_expected = True)
			self.active_view = None
			self.active_view_arg = None
			self.active_view_update_rate = None
			self.active_view_terminate = None
		else:
			self.display_lines = ['Align Star %s' % starNum, 'Select star in SkySafari', 'away from NCP and', 'goto and Align']


	def view_spiral_search(self, arg):
		self.display_lines = ['Spiral search in progress,', 'press any button to halt.', 'Change speed with joystick', 'rate prior to search.']


	def view_site(self, arg):
		lat = self.conman.send_command('GtH', reply_expected = True)
		lon = self.conman.send_command('GgH', reply_expected = True)
		self.display_lines = ['Latitude: %s' % lat, 'Longitude: %s' % lon]


	def terminate_spiral_search(self):
		self.conman.send_command('Qn', reply_expected = False)


	def confirmation_view(self, lines):
		self.display_lines = lines


	def process(self, buttonsPressed, buttonsReleased, buttonsHeld):
		self.status_changed = False
		self.needs_display = False

		(used, statusButtonsPressed) = self.process_status(buttonsPressed, buttonsReleased, buttonsHeld)
		buttonsPressed = statusButtonsPressed
		if not used:
			if 'C' in buttonsPressed:
				# Toggle Normal/Joystick when center key is pressed
				if self.mode == self.MODE_JOYSTICK:
					self.mode = self.MODE_NORMAL
					buttonsPressed = []
					self.conman.send_command('Q', reply_expected = False)	# Stop motion
					self.active_view = None
					self.active_view_arg = None
					self.active_view_terminate = None
					self.needs_display = True
				else:
					self.mode = self.MODE_JOYSTICK
					buttonsPressed = []
					self.last_joystick_tx = time.monotonic()
					self.conman.send_command('R%d' % self.guide_rate, reply_expected = False)      # Set guide rate
					self.active_view = self.view_joystick
					self.active_view_arg = None
					self.active_view_update_rate = 1
					self.active_view_terminate = None
					self.active_view(self.active_view_arg)
					self.needs_display = True

                	(used, clearButtons) = self.process_views(buttonsPressed, buttonsReleased, buttonsHeld)

			if used and clearButtons:
				# If we have an active view and a button is pressed, we need to return to displaying the menu and remove the buttons from input
				self.active_view = None
				self.needs_display = True
				used = False
				buttonsPressed = []
		if not used:
                	self.process_menus(buttonsPressed, buttonsReleased, buttonsHeld)
