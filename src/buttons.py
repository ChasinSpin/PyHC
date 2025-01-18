import board
import digitalio
from adafruit_debouncer import Debouncer



class Buttons():

	BUTTON_F1	= 0
	BUTTON_F2	= 1
	BUTTON_NORTH	= 2
	BUTTON_SOUTH	= 3
	BUTTON_EAST	= 4
	BUTTON_WEST	= 5
	BUTTON_CENTER	= 6
	BUTTON_SIZE	= BUTTON_CENTER + 1

	BUTTON_BOARD_PINS = [board.D5, board.D6, board.D9, board.D10, board.D11, board.D12, board.A5]
	BUTTON_NAMES	  = ['F1', 'F2', 'N', 'S', 'E', 'W', 'C']


        def __init__(self):
		if len(self.BUTTON_BOARD_PINS) != self.BUTTON_SIZE:
			raise ValueError('BUTTON_SIZE and BUTTON_BOARD_PINS mismatch in length')
		if len(self.BUTTON_NAMES) != self.BUTTON_SIZE:
			raise ValueError('BUTTON_SIZE and BUTTON_NAMES mismatch in length')

		self.buttons = []

		for i in range(0, self.BUTTON_SIZE):
			(pin, button) = self.__createButton(self.BUTTON_BOARD_PINS[i])
			self.buttons.append( { 'name': self.BUTTON_NAMES[i], 'button': button, 'pin': pin } )
		#print(self.buttons)


	def __createButton(self, boardPin):
                pin		= digitalio.DigitalInOut(boardPin)
                pin.pull	= digitalio.Pull.UP
                button		= Debouncer(pin, interval = 0.02)
		return (pin, button)


        def process(self):
		""" Returns a tuple of arrays containing the buttons pressed, released and held """

		# Read the buttons
		pressed = []
		released = []
		held = []

		for i in range(0, self.BUTTON_SIZE):
			button	= self.buttons[i]['button']
			name 	= self.buttons[i]['name']

			button.update()

			if button.fell:
				pressed.append(name)
			if button.rose:
				released.append(name)
			if not button.value:
				held.append(name)
				
		return (pressed, released, held)
