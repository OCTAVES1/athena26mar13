from scapy.all import sniff,ARP,Padding

print("[*] Crypto-Receiver Listening for encrypted ARP padding...")

psk = b"WOLF" # Must match the sender's key

def xor_cipher(data,key):
	return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def extract_encrypted_padsteg(packet):
	if packet.haslayer(ARP) and packet.haslayer(Padding):
		raw_padding = packet[Padding].load

		#Grab out exact 18-byte payload block
		ciphertext=raw_padding[:18]
		
		#Decrypt the data using our PSK
		decrypted_bytes=xor_cipher(ciphertext,psk)
	
		try:
			#Attept to decode to text
			payload = decrypted_bytes.decode('utf-8').strip('\x00')

			#Filter out standard network noise by checking if it contains our specific string format
			# (In a real scenario,you'd use a magic header, but this works perfectly for the demo)
			if payload.isprintable() and len(payload) > 5:
				print(f"\n[+] ENCRYPTED GHOST INTERCEPTED!")
				print(f"	SOURCE IP claim: {packet[ARP].psrc}")
				print(f"	Raw Hex on Wire: {ciphertext.hex()}")
				print(f"	Decrypted: {payload}")
		except UnicodeDecodeError:
			pass
sniff(iface="h2-eth0",filter="arp",prn=extract_encrypted_padsteg,store=0)

