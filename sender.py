from scapy.all import Ether,sendp,raw 

print("[*] Initializing Covert Layer 2 Sender...")

#1. Define the parameters
#Using the experimental EtherType 0x77B5 as per the architecture doc ethertype=0x88b5
ethertype=0x88b5
target_mac="ff:ff:ff:ff:ff:ff" #Broadcast MAC for testing
clandestine_payload=b"HACKATHON_PROTOTYPE_INITIATED"

#2.Construct the Ethernet frame
#We stack the payload directly onto the custom Ether header
covert_frame=Ether(dst=target_mac,type=ethertype) /clandestine_payload

#3.Inject the frame at Layer 2
#sendp() places the raw frame directly onto the interface,bypassing the OS routing 
print(f"[*] Injecting payload:{clandestine_payload}")
sendp(covert_frame,iface="h1-eth0",verbose=True)

print("[+] Transmission Complete.")

