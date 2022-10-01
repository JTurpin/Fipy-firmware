# Setup Global constants and variables
PRODUCT_ID_CONST=10253
PRODUCT_VERSION_NUMBER=7

# map human names of products to their ids
BORON_3_CHANNEL=10253
BORON_18_CHANNEL=11532
ARGON_3_CHANNEL=11842
ARGON_18_CHANNEL=11632

# arbitrary numbers to represent device types
BORON=1000
ARGON=1001
FIPY=1002

# setup config for firmware depending on the product id
if PRODUCT_ID_CONST==BORON_3_CHANNEL
	CHANNEL_COUNT=3
	DEVICE_TYPE=BORON
elif PRODUCT_ID_CONST==BORON_18_CHANNEL
	CHANNEL_COUNT=18
	DEVICE_TYPE=BORON
elif PRODUCT_ID_CONST==ARGON_3_CHANNEL
	CHANNEL_COUNT=3
	DEVICE_TYPE=ARGON
elif PRODUCT_ID_CONST==ARGON_18_CHANNEL
	CHANNEL_COUNT=18
	DEVICE_TYPE=ARGON
else:
	print("there was an error setting up the product")


# ---- State Machine states ----
# attempt to reconnect for a certain amount of time before doing STATE_RESET_DEVICE
STATE_ATTEMPT_CONNECT=0
# sync device time with UTC via Particle api
STATE_SYNC_CLOCK=1
# ready data from the meter and publish it if connected (add to post queue if not connected)
STATE_QUERY_METER=2
# sleep for defined amount between posts
STATE_SLEEP=3
# power off device
STATE_RESET_DEVICE=4

# Address of the meter. Must match the set COM address on the accurev device
METER_ADDRESS = 200;

# millisecond delay after a failure before trying to read again
FAILURE_DELAY = 1000;

# size of json buffer in bytes
JSON_BUFFER_SIZE = 2048;

# millisecond delay between meter reads
extern int cycleDelay;

# baudRate for communicating with the meter device
extern int baudRate;

# bool flag for tracing whether we have enabled updates yet
extern bool updatesEnabled;

# last time we synced the clock with particle
extern unsigned long lastSync;

# current state in device state machine
extern String status;

# tracks current state. Value set here will be the initial state upon powering on
extern volatile int currentState;

if CHANNEL_COUNT == 3
    # dictionary of string names of registers to their addresses
    channelDict = {
    "Isc": "0x104B", # Current Scale Factor
    "Vsc": "0x1054", # Voltage Scale Factor
    "Pt": "0x1057", # Total Real Power
    "Psc": "0x105B", # Real Power Scale Factor
    "PFsc": "0x106A", # Power Factor Scale Factor

    "Van": "0x104D", # Phase Voltage AN
    "Vbn": "0x104E", # Phase Voltage BN
    "Vcn": "0x104F", # Phase Voltage CN
    "Vab": "0x1051", # Phase A-B Line to Line voltage
    "Vbc": "0x1052", # Phase B-C Line to Line voltage
    "Vca": "0x1053", # Phase C-A Line to Line voltage

    "I1": "0x1048", # Amps Phase A
    "I2": "0x1049", # Amps Phase B
    "I3": "0x104A", # Amps Phase C
    "P1": "0x1058", # Watts Phase A
    "P2": "0x1059", # Watts Phase B
    "P3": "0x105A", # Watts Phase C
    "PF1": "0x1067", # PF Phase A
    "PF2": "0x1068", # PF Phase B
    "PF3": "0x1069", # PF Phase C
    }
elif CHANNEL_COUNT == 18
    # maps string names of registers to their addresses
    # non-channel related data
    channelDict = {
    "Pt": "0x201A", #Total Real Power

    "Van": "0x2002", #Phase A Line-Neutral Voltage
    "Vbn": "0x2004", #Phase B Line-Neutral Voltage
    "Vcn": "0x2006", #Phase C Line-Neutral Voltage

    "Vab": "0x200A", #Phase A-B Line to Line voltage
    "Vbc": "0x200C", #Phase B-C Line to Line voltage
    "Vca": "0x200E", #Phase C-A Line to Line voltage

    // channel data
    "P1": "0x2102", #Channel  1 Real Power
    "P2": "0x210E", #Channel  2 Real Power
    "P3": "0x211A", #Channel  3 Real Power
    "P4": "0x2126", #Channel  4 Real Power
    "P5": "0x2132", #Channel  5 Real Power
    "P6": "0x213E", #Channel  6 Real Power
    "P7": "0x214A", #Channel  7 Real Power
    "P8": "0x2156", #Channel  8 Real Power
    "P9": "0x2162", #Channel  9 Real Power
    "P10": "0x216E", #Channel 10 Real Power
    "P11": "0x217A", #Channel 11 Real Power
    "P12": "0x2186", #Channel 12 Real Power
    "P13": "0x2192", #Channel 13 Real Power
    "P14": "0x219E", #Channel 14 Real Power
    "P15": "0x21AA", #Channel 15 Real Power
    "P16": "0x21B6", #Channel 16 Real Power
    "P17": "0x21C2", #Channel 17 Real Power
    "P18": "0x21CE", #Channel 18 Real Power

    "I1": "0x2100", #Channel  1 Current
    "I2": "0x210C", #Channel  2 Current
    "I3": "0x2118", #Channel  3 Current
    "I4": "0x2124", #Channel  4 Current
    "I5": "0x2130", #Channel  5 Current
    "I6": "0x213C", #Channel  6 Current
    "I7": "0x2148", #Channel  7 Current
    "I8": "0x2154", #Channel  8 Current
    "I9": "0x2160", #Channel  9 Current
    "I10": "0x216C", #Channel 10 Current
    "I11": "0x2178", #Channel 11 Current
    "I12": "0x2184", #Channel 12 Current
    "I13": "0x2190", #Channel 13 Current
    "I14": "0x219C", #Channel 14 Current
    "I15": "0x21A8", #Channel 15 Current
    "I16": "0x21B4", #Channel 16 Current
    "I17": "0x21C0", #Channel 17 Current
    "I18": "0x21CC", #Channel 18 Current

    "PF1": "0x2108", #Channel  1 Power Factor
    "PF2": "0x2114", #Channel  2 Power Factor
    "PF3": "0x2120", #Channel  3 Power Factor
    "PF4": "0x212C", #Channel  4 Power Factor
    "PF5": "0x2138", #Channel  5 Power Factor
    "PF6": "0x2144", #Channel  6 Power Factor
    "PF7": "0x2150", #Channel  7 Power Factor
    "PF8": "0x215C", #Channel  8 Power Factor
    "PF9": "0x2168", #Channel  9 Power Factor
    "PF10": "0x2174", #Channel 10 Power Factor
    "PF11": "0x2180", #Channel 11 Power Factor
    "PF12": "0x218C", #Channel 12 Power Factor
    "PF13": "0x2198", #Channel 13 Power Factor
    "PF14": "0x21A4", #Channel 14 Power Factor
    "PF15": "0x21B0", #Channel 15 Power Factor
    "PF16": "0x21BC", #Channel 16 Power Factor
    "PF17": "0x21C8", #Channel 17 Power Factor
    "PF18": "0x21D4", #Channel 18 Power Factor
    }

