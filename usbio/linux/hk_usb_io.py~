#!/usr/bin/python
import usb.core
import usb.util
from array import array
import sys
import time

_mod_ver  = '0.1'		# python HKUSBIO module version
_mod_date = '2/13/2013'	# module date
u_ad0 = 0x37	# read ADC value from RA0
u_ad1 = 0x38	# read ADC value from RA1
u_rom = 0x85	# get PIC rom version
u_led = 0x80	# toggle LED 
u_swc = 0x81	# get switch pressed or not
u_gpd = 0x84	# configure GPIO direction on a pin
u_gpi = 0x82	# read value on GPIO pin
u_gpo = 0x83	# write value to GPIO pin
u_uss = 0x86	# send a string to the UART
u_tst = 0x87	# test if UART has a char available
u_urc = 0x88	# read a single char from UART
u_usc = 0x89	# send a single char to the UART
rd4 = 1		# GPIO pin rd4	def=input
rd5 = 2		# GPIO pin rd5	def=input
rd6 = 3		# GPIO pin rd6	def=output
rd7 = 4		# GPIO pin rd7	def=output
dir_output = 0	# control GPIO pin direction
dir_input  = 1
def init():							# setup USB device structure
	# find our device
	dev = usb.core.find(idVendor=0x04d8, idProduct=0x003f)
	# was it found
	if dev is None:
		raise ValueError('Device not found')
	# handle if device is busy
	if dev.is_kernel_driver_active(0) is True:
		dev.detach_kernel_driver(0)
	# set the active configuration.  No args the first config
	# will become the active one
	dev.set_configuration()
	return dev
def module_version():
	a = 'Version: ' + _mod_ver + ', Date: ' + _mod_date
	return a
def rom_version(dev):				# get PIC ROM version
	# read ROM version 
	dev.write(1, [u_rom], 0, 100)
	ret = dev.read(0x81, 64, 0, 100)
	rom_version = ''
	rom_version += chr(ret[1])
	rom_version += '.'
	rom_version += chr(ret[2])
	rom_version += chr(ret[3])
	return rom_version
def toggle_led(dev):				# toggle LED
	dev.write(1, [u_led], 0, 100)
def read_switch(dev):				# read switch press
	dev.write(1, [u_swc], 0, 100)
	sw = dev.read(0x81, 64, 0, 100)
	if (sw[1] == 0):
		 return True
	else:
		 return False
def gpio_init(dev,pin,pdir):		# set GPIO direction on pin
	dev.write(1,[u_gpd, pin, pdir], 0, 100)
def gpio_out(dev,pin):				# otuput a value on GPIO pin
	dev.write(1, [u_gpo, pin, 1], 0, 100)
def gpio_in(dev,pin):				# read value on GPIO pin
	dev.write(1,[u_gpi, pin], 0, 100)
	ret = dev.read(0x81, 64, 0, 100)
	return ret[1]
def adc_ra0(dev):					# do ADC conversion on RA0
	dev.write(1,[u_ad0], 0, 100)
	ret = dev.read(0x81, 64, 0, 100)
	value = ret[2] << 8
	value = value | ret[1]
	return value
def adc_ra1(dev):					# do ADC conversion on RA0
	dev.write(1,[u_ad1], 0, 100)
	ret = dev.read(0x81, 64, 0, 100)
	value = ret[2] << 8
	value = value | ret[1]
	return value
def ser_test(dev):					# check if a char available on serial port
	dev.write(1, [u_tst], 0, 100)
	ret = dev.read(0x81, 64, 0, 100)
	return ret[1]
def ser_putc(dev,schar):			# send a char to the serial port
	a = map( ord, schar)
	a.insert(0, u_usc)
	dev.write(1, a, 0, 100)
def ser_puts(dev, strval):			# send a string to the serial port
	a = map( ord, strval)
	a.insert(0, u_uss)
	a.append(0)
	dev.write(1, a, 0, 100)
def ser_getc(dev):					# get a single char from the serial port
	dev.write(1, [u_urc], 0, 100)
	ret = dev.read(0x81, 64, 0, 100)
	return ret[1]
def close(dev):						# reset USB device
	dev.reset()

#===================== end of module =========
usb = init()			# init the USB IO board

print module_version()

print rom_version(usb)		# print rom version

toggle_led(usb)			# toggle the LED

a = read_switch(usb)		# read the switch status
print a

gpio_init(usb,rd7,dir_input)	# configure gpio RD7 as input
a = gpio_in(usb,rd7)		# read the GPIO pin RD7
print a

a = adc_ra1(usb)		# do ADC conversion on pin RA1
print a

# LCD on serial port (UART IO to a serial attached LCD)
ser_putc(usb,chr(0xfe))		# clear LCD screen
ser_putc(usb,chr(0x01))	
ser_putc(usb,chr(0xfe))		# block cursor
ser_putc(usb,chr(0x0d))
ser_puts(usb,"Hello World")
ser_puts(usb,chr(0xfe) + chr(192))	# move to next line
ser_puts(usb,"From Odroid-x2")

if (ser_test(usb)):		# check if incoming char on UART
	a = ser_getc(usb)
	print a
else:
	print "no"

close(usb)
