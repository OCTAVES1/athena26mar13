from scapy.all import sniff,Ether,raw

print("[*} Covert Receiver Listening for 0x88b5 frames..")

def extract_payload(packet):
	#Double-check we have the right EtherType (though the BPF filter should catch this)
	if packet.haslayer(Ether) and packet[Ether].type==0x88b5:
		#Extract the raw bytes and decode them into readable text
		payload=raw(packet.payload).decode('utf-8',errors='ignore')
		mac_source=packet[Ether].src
		
		print(f"[+] INTERCEPTED! Source MAC: {mac_source} | Payload:{payload}")

#The sniff function listens on the interface
#Filter="Ether proto  0x88b5"tells the kernel to  ONLY pass us our custom frames, ignoring standard LAN noise.
sniff(iface="h2-eth0",filter="ether proto 0x88b5",prn=extract_payload,store=0)


