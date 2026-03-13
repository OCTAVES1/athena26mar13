from scapy.all import sniff, Ether
import time
import os
 
# 1. Setup the secret code and the log file
COVERT_ETHERTYPE = 0x0806 
LOG_FILE = "ids_alert_log.csv"
 
# 2. Create the log file with headers if it doesn't exist yet
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("Time,Source_MAC,Destination_MAC,Alert\n")
 
# 3. The scanner function (The God-Mode Wiretap)
def check_packet(packet):
    # Only look at Layer 2 Ethernet frames
    if packet.haslayer(Ether):
        # Did we catch the secret 0x88B5 code?
        if packet[Ether].type == COVERT_ETHERTYPE:
            current_time = time.strftime('%H:%M:%S')
            src = packet[Ether].src
            dst = packet[Ether].dst
            
            # Print a massive red alert to the terminal screen!
            print(f" [{current_time}] COVERT PACKET DETECTED! From: {src} To: {dst}")
            
            # Save it to the CSV so your Dashboard UI can read it
            with open(LOG_FILE, "a") as f:
                f.write(f"{current_time},{src},{dst},Covert L2 Frame\n")
 
# 4. Start the engine
print(" Backend IDS is online and listening on BOTH doors (s1-eth1 and s1-eth2)...")
 
# Listening to a list of interfaces to catch two-way traffic!
sniff(iface=["s1-eth1", "s1-eth2"], prn=check_packet, store=False)

