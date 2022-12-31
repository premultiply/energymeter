#!/usr/bin/python3
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

##### Pin GPIO3 #####
# impulses per kWh
impkwh3 = 1000
# total count of pulses
energy3 = 0
# peak power between two pulses
power3 = 0
# timestamp of last pulse
ltime3 = time.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)
#GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# handle interrupt
def isrpulse3(channel):
        global energy3, power3, ltime3
        energy3 += 1
        ctime = time.time()
        power3 = 3600 / (ctime - ltime3)
        ltime3 = ctime


# setup IRQ routine
GPIO.add_event_detect(3, GPIO.RISING, callback = isrpulse3, bouncetime = 30)
#####################


if __name__ == "__main__":
        try:
                while True:
                        # precise timing of 1 second interval
                        time.sleep(1 - time.time() % 1)
                        # limit measurment duration for pulse distance
                        dtime = time.time() - ltime3
                        lpower = 0 if dtime > 60 else power3
                        with open("/run/meter_power3", "w") as power3_file:
                                power3_file.write("%0.3f" % (lpower*(1000/impkwh3)))
                        with open("/run/meter_energy3", "w") as energy3_file:
                                energy3_file.write("%0.3f" % (energy3*(1000/impkwh3)/1000))

        except (KeyboardInterrupt, SystemExit):
                # handle process termination and CTRL+C
                ##### Pin GPIO3 #####
                GPIO.remove_event_detect(3)
                #####################
                GPIO.cleanup()
