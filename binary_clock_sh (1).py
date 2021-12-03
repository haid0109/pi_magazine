#!/usr/bin/env python

from sense_emu import SenseHat, ACTION_PRESSED
import signal, sys, argparse, time, datetime

hat = SenseHat()

def end(signum, frame):
	hat.show_message('END')
	sys.exit(0)

signal.signal(signal.SIGTERM, end)
signal.signal(signal.SIGINT, end)

hour_color = (0, 255, 0)
minute_color = (0, 0, 255)
second_color = (255, 0, 0)
red_color = (255, 0, 0)
off = (0, 0, 0)

display_mode = 'horizontal'
time_mode = 24
columns = 3

parser = argparse.ArgumentParser()

parser.add_argument('--display', type=str)
parser.add_argument('--time', type=int)
parser.add_argument('--columns', type=int)

arguments = parser.parse_args()

display_argument = getattr(arguments, 'display')
time_argument = getattr(arguments, 'time')
columns_argument = getattr(arguments, 'columns')

if(display_argument != None and (display_argument == 'horizontal' or display_argument == 'vertical')): display_mode = display_argument
if(time_argument != None and (time_argument == 24 or time_argument == 12)): time_mode = time_argument
if(columns_argument != None and (columns_argument == 3 or columns_argument == 6)): columns = columns_argument

hat.clear()

hat.show_message('START')

def display_binary(value, index, color):
	binary_str = "{0:8b}".format(value)
	for x in range(1, 8):
		if binary_str[x] == '1':
			if(display_mode == 'horizontal'):
				hat.set_pixel(x, index, color)
			else:
				hat.set_pixel(index, x, color)
		else:
			if(display_mode == 'horizontal'):
				hat.set_pixel(x, index, off)
			else:
				hat.set_pixel(index, x, off)

def horizontal_press(event):
	global display_mode
	if(event.action == ACTION_PRESSED):
		if(display_mode == 'horizontal'):
			display_mode = 'vertical'
		else:
			display_mode = 'horizontal'

def vertical_press(event):
	global columns
	if(event.action == ACTION_PRESSED):
		if(columns == 3):
			columns = 6
		else:
			columns = 3

def pushed_middle(event):
	global time_mode
	if(event.action == ACTION_PRESSED):
		if(time_mode == 24):
			time_mode = 12
		else:
			time_mode = 24

hat.stick.direction_right = hat.stick.direction_left = horizontal_press
hat.stick.direction_down = hat.stick.direction_up = vertical_press
hat.stick.direction_middle = pushed_middle

while True:
	hat.clear()

	t = datetime.datetime.now()
	if(time_mode == 12 and t.hour >= 12):
		t -= datetime.timedelta(hours=12)
		hat.set_pixel(0, 0, red_color)
	else:
		hat.set_pixel(0, 0, off)

	if(columns == 3):
		display_binary(t.hour, 3, hour_color)
		display_binary(t.minute, 4, minute_color)
		display_binary(t.second, 5, second_color)
	else:
		display_binary(t.hour // 10, 1, hour_color)
		display_binary(t.hour % 10, 2, hour_color)
		display_binary(t.minute // 10 , 3, minute_color)
		display_binary(t.minute % 10, 4, minute_color)
		display_binary(t.second // 10, 5, second_color)
		display_binary(t.second % 10, 6, second_color)
	time.sleep(0.5)
