#!/usr/bin/python
# -*- coding: utf-8 -*-

# ENERGYMETER für S0-Schnittstelle am RaspberryPi
# für Zähler mit 1000 Imp/kWh bzw. 1 Imp/Wh
#
# Primäre S0-Schnittstelle: PIN5(GPIO3) S0+, PIN6(GND) S0-
# Option für weitere S0-Schnittstelle: PIN3(GPIO2) SO+ und GND SO-
# GPIO3 und GPIO2 haben feste interne 1,8kOhm Pullup-Widerstände
#
# 100nF-Kondensator zwischen Pin und GND verringert EMV-Einsteuungen (Fehlimpulse)

import RPi.GPIO as GPIO
import time
import sys
import rrdtool

##### Pin GPIO3 #####
# total count of pulses
count3 = 0
# peak power between two pulses
power3 = 0
# timestamp of last pulse
ltime3 = time.time()

t1count3 = 0
t2count3 = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)
#GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# handle interrupt
def isrcount3(channel):
	global count3, power3, ltime3
	count3 += 1
	ctime = time.time()
	power3 = 3600 / (ctime - ltime3)
	ltime3 = ctime
	#print "count3: " + str(count3) + "; power3: " + str(power3)

# setup IRQ routine
GPIO.add_event_detect(3, GPIO.RISING, callback = isrcount3, bouncetime = 30)
#####################


try:
	while True:
		# precise timing of 1 minute interval
		time.sleep(60 - time.time() % 60)
		
		##### Pin GPIO3 #####
		# absolute count during interval
		t2count3 = count3
		energy3 = t2count3 - t1count3
		t1count3 = t2count3
		
		# limit measurment duration for pulse distance
		dtime = time.time() - ltime3
		if dtime > 60:
			power3 = 3600 / dtime if dtime < 600 else 0
		#####################
		
		# output to stdout as CSV compatible line
		print time.strftime('%Y-%m-%d %H:%M:%S') + ";%s;%s;%s" %(energy3, power3, count3)

		# update RRD
		rrdtool.update(sys.argv[1], "N:%s:%s:%s" %(energy3, power3, count3))

except (KeyboardInterrupt, SystemExit):
	# handle process termination and CTRL+C
	##### Pin GPIO3 #####
	GPIO.remove_event_detect(3)
	#####################
	GPIO.cleanup()
