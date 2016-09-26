#!/usr/bin/python

from subprocess import call
import datetime
import time
import bluetooth
import sys
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Screen(object):
	def __init__(self):
		self._locked = False
		
	def lock(self):
		if not self._locked:
			self._locked = True
			call(["gnome-screensaver-command", "-l"])
			# TODO: if screensaver not available, then run os.system("xset dpms force off")
			os.system("xset dpms force off")
			call(["gnome-screensaver-command", "-a"])

	def unlock(self):
		if self._locked:
			self._locked = False
			call(["gnome-screensaver-command", "-d"])
			os.system("xset dpms force on")
		

class Mesin(object):
	def __init__(self):
		self.screen = Screen()

		self._btAddr = None
		self._btInRange = False
		self._scanPeriod = 3
		self._timeout = 5
		self._locked = False

	def discover_devices(self):
		return bluetooth.discover_devices(duration=8, flush_cache=True, lookup_names=True)
		
	def main(self):
		print "Searcing devices . . ."
		result = self.discover_devices()
		if result:
			while True:
				no = 1
				print "Select your bluetooth device!"
				for addr, name in result:
					print "   ",str(no)+".\t"+"%s - %s" % (name, addr)
					no += 1
				print "Choice :",
				num = input()
				if num > 0 and num <= len(result):
					break
			
			addr, name = result[num-1]
			self._btAddr = addr
			print "Listening to", name

		try:
			btName =  bluetooth.lookup_name(self._btAddr,timeout=self._timeout)
			if btName:
				while True:
					who =  bluetooth.lookup_name(self._btAddr,timeout=self._timeout)

					if who:
						self.screen.unlock()
						self._btInRange = True
					else:
						self.screen.lock()
						self._btInRange = False

					time.sleep(self._scanPeriod)
					if self._btInRange:
						print bcolors.OKGREEN+str(self._btInRange)+bcolors.ENDC, '|', who, '|', datetime.datetime.now().strftime("%A, %d %B %Y %H:%M:%S")
					else:
						print bcolors.FAIL+str(self._btInRange)+bcolors.ENDC, '|', who, '|', datetime.datetime.now().strftime("%A, %d %B %Y %H:%M:%S")

			else:
				print 'ERROR: bluetooth device not found'
				sys.exit
		except Exception, err:
			print err

#main
if __name__ == "__main__":
	bt = Mesin()
	bt.main()
