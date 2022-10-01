"""
Allumia FiPy Firmware


FiPy -> RS485 (MAX9485CSA)
P3 -> DI
P4 -> RO
P8 -> DE/RE jumped
5V -> VCC
GND -> GND

FiPy -> RTC (DS3231M)
3v3 -> 3v3
P21  -> SDA
P22 -> SCL
GND -> GND

FiPy -> SD Card (SPI)
3v3 -> 3v3
P14 -> MISO
P11 -> MOSI
P10 -> SCK
GND -> GND



classmachine.SDCard(slot=1, width=1, cd=None, wp=None, sck=None, miso=None, mosi=None, cs=None, freq=20000000)¶
This class provides access to SD or MMC storage cards using either a dedicated SD/MMC interface hardware or through an SPI channel. The class implements the block protocol defined by os.AbstractBlockDev. This allows the mounting of an SD card to be as simple as:

os.mount(machine.SDCard(), "/sd")

The constructor takes the followi-ng parameters:
    slot selects which of the available interfaces to use. Leaving this unset will select the default interface.
    width selects the bus width for the SD/MMC interface.
    cd can be used to specify a card-detect pin.
    wp can be used to specify a write-protect pin.
    sck can be used to specify an SPI clock pin.
    miso can be used to specify an SPI miso pin.
    mosi can be used to specify an SPI mosi pin.
    cs can be used to specify an SPI chip select pin.
    freq selects the SD/MMC interface frequency in Hz (only supported on the ESP32).





from machine import I2C # used for i2c 
from machine import SPI # used for SD card

import utime # used for MAX485
import ModBus # used for MAX485
from machine import UART # used for MAX485


# configure the SPI master @ 2MHz
# this uses the SPI non-default pins for CLK, MOSI and MISO (``P19``, ``P20`` and ``P21``)
spi = SPI(0, mode=SPI.MASTER, baudrate=2000000, polarity=0, phase=0, pins=('P10','P11','P14'))
spi.write(bytes([0x01, 0x02, 0x03, 0x04, 0x05])) # send 5 bytes on the bus
spi.read(5) # receive 5 bytes on the bus
rbuf = bytearray(5)
spi.write_readinto(bytes([0x01, 0x02, 0x03, 0x04, 0x05]), rbuf) # send a receive 5 bytes


i2c = I2C(0, pins=('P10','P11'))     # create and use non-default PIN assignments (P10=SDA, P11=SCL)
i2c.init(I2C.MASTER, baudrate=20000) # init as a master
i2c.deinit()                         # turn off the peripheral

# Import globals
import globals

#######################################
######### RS485 Configuration #########
#######################################

# UART docs are located here: https://docs.pycom.io/firmwareapi/pycom/machine/uart/
uart = UART(1, baudrate=9600)
# this uses the UART_1 non-default pins for TXD, RXD, RTS and CTS (``P20``, ``P21``, ``P22``and ``P23``)
uart.init(9600, bits=8, parity=None, stop=1,pins=('P3','P4','P8',None))
instrument = ModBus.Instrument(uart,0x01,mode=ModBus.MODE_RTU)
print(instrument)
v = instrument.read_registers(2,2)
print(v)

# create channel output
# Dictionary of lists
meterReadings = {

}


thislist = ["apple", "banana", "cherry"]

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"color": "red"})


"""

import pycom
import time

pycom.heartbeat(False)

while True:
  pycom.rgbled(0x7f0000) # red
  time.sleep(0.5)
  pycom.rgbled(0x007f00) # green
  time.sleep(0.5)
  pycom.rgbled(0x00007f) # blue
  time.sleep(0.5)
