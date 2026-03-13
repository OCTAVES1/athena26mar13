from scapy.all import Ether, ARP,sendp,Padding

print("[*] Initializing PadSteg Sender..")
#1.Forge a totally normal-looking ARP Request (28 bytes)
#We ask "Who has 10.0.0.2?" to make it look like standard network discovery
arp_req=ARP(pdst="10.0.0.2")

#2. Define the Covert Payload
#We have exactly 18 bytes of padding space before teh frame gets suspiciously large.
covert_data=b"GHOST_IN_THE_WIRE!"

#3.Construct the Steganographic Frame
#Stack:Standard Ethernet +Standard ARP +Hijiacked Padding
frame=Ether(dst="ff:ff:ff:ff:ff:ff") / arp_req / Padding(load=covert_data)

#4. Inject it onto the wire
print(f"[*] Injecting Padsteg Payload:{covert_data}")
sendp(frame,iface="h1-eth0",verbose=False)

print("[+] Ghost Frame Transmitted.")

