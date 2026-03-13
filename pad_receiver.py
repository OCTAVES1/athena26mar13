from scapy.all import sniff, ARP, Padding

print("[*] Padsteg Receiver Listening for covert ARP padding..")

def extract_padsteg(packet):
	#Only inspect ARP packet that have a Padding layer attached
	if packet.haslayer(ARP) and packet.haslayer(Padding):
		#Extract the raw padding bytes
		raw_padding=packet[Padding].load

		try:
			#Decode the bytes and strip out any standard null/zero padding (\x00)
			payload=raw_padding.decode('utf-8').strip('\x00')

			#If there's text left over,we caught a ghost!
			if payload:
				print(f"\n[+] GHOST INTERCEPTED!")
				print(f" Source IP claim:{packet[ARP].psrc}")
				print(f" Hidden Data:	{payload}")
		except UnicodeDecodeError:
		 #if it can't be decoded to text,it's just normal network padding.Ignore it.
			pass

#The BPF filter "arp" guarantees we only listen to ARP traffic,dropping everything else.
sniff(iface="h2-eth0",filter="arp",prn=extract_padsteg,store=0)

