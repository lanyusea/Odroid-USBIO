#!/usr/bin/python
# Markham Thomas  2/17/2013
# SFR test program
from hk_usb_io import *
import sys
import time

usb = init()			# init the USB IO board

print module_version()		# print python module version

print rom_version(usb)		# print rom version
print "---------- output -----------"

a = sfr_get_reg(usb, 0xcf)
print hex(a)
