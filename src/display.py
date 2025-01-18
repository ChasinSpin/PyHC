import time
import board
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from displayio import Group



class Display():

        LINES_Y = [20, 50, 80, 110]	# Location in pixels for each of the 4 lines
	TEXT_COLORS = { 'white': 0xFFFFFF, 'red': 0xFF0000, 'green': 0x00FF00, 'blue': 0x0000FF, 'yellow': 0xFFFF00, 'cyan': 0x00FFFF, 'magneta': 0xFF00FF }

        def __init__(self, version, display_color, info_text):
                self.systemDisplay	= board.DISPLAY
                self.font		= bitmap_font.load_font("fonts/Helvetica-Bold-16.bdf")
		self.text_color		= self.TEXT_COLORS[display_color]

                group = Group()

                group.append(self.__makeTextArea(info_text, self.text_color, 0, self.LINES_Y[0]))
                group.append(self.__makeTextArea('Version: %s' % version, self.text_color, 0, self.LINES_Y[2]))
                group.append(self.__makeTextArea('Author: @ChasinSpin', self.text_color, 0, self.LINES_Y[3]))
                self.systemDisplay.root_group = group

                time.sleep(2)


        def __makeTextArea(self, text, color, x, y):
                text_area = label.Label(self.font, text=text, color=color)
                text_area.x = x
                text_area.y = y
                return text_area


	def display_connecting(self, connection_method, wifi_ssid):
                group = Group()
                group.append(self.__makeTextArea('Connecting to WiFi', self.text_color, 0, self.LINES_Y[0]))
                group.append(self.__makeTextArea('network: %s' % wifi_ssid, self.text_color, 0, self.LINES_Y[1]))
                self.systemDisplay.root_group = group


	def display_menu(self, lines):
                group = Group()
		line_index = 0
		for line in lines:
			if line_index >= 4:
				return
                	group.append(self.__makeTextArea(line, self.text_color, 0, self.LINES_Y[line_index]))
			line_index += 1
                self.systemDisplay.root_group = group


	def display_position(self, ra, dec, az, alt):
                group = Group()
                group.append(self.__makeTextArea('RA:  %s' % ra,  self.text_color, 0, self.LINES_Y[0]))
                group.append(self.__makeTextArea('DEC: %s' % dec, self.text_color, 0, self.LINES_Y[1]))
                group.append(self.__makeTextArea('AZ:  %s' % az,  self.text_color, 0, self.LINES_Y[2]))
                group.append(self.__makeTextArea('ALT: %s' % alt, self.text_color, 0, self.LINES_Y[3]))
                self.systemDisplay.root_group = group
