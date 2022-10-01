import pycom
from network import WLAN
from network import MDNS
import machine
import time
import secrets 


# modbus via sunspec
# https://www.accuenergy.com/support/modbus-map/
# https://pysunspec.readthedocs.io/en/latest/pysunspec.html#interacting-with-a-sunspec-device

#pycom.heartbeat(False)

#def stop_light():
#    #for cycles in range(2): # stop after 10 cycles
#    pycom.rgbled(0x007f00) # green
#    time.sleep(1)
#    pycom.rgbled(0x7f7f00) # yellow
#    time.sleep(1)
#    pycom.rgbled(0x7f0000) # red
#    time.sleep(1)

### CONFIGURE NETWORK ###
#You can set this to True if Pybytes connects to your router already, and skip the rest
#pycom.pybytes_on_boot(False) 

#pycom.smart_config_on_boot(False)
#pycom.wifi_on_boot(True)
#pycom.wifi_mode_on_boot(WLAN.STA)
#pycom.wifi_ssid_sta('YIMMY-EXT')
#pycom.wifi_pwd_sta('Wh0pharted')

### Call stop_light ###
#stop_light()


### Secondary config for wireless ###
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='YIMMY-EXT', auth=(WLAN.WPA2, 'Wh0pharted'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())


time.sleep(5)

### CONFIGURE MDNS ###
MDNS.init()
MDNS.set_name(hostname ="fipy", instance_name="fipy")
MDNS.add_service("_http",MDNS.PROTO_TCP, 80)
MDNS.add_service("_telnetd", MDNS.PROTO_TCP, 23)

time.sleep(10)

wlan.ifconfig()
#machine.reset()