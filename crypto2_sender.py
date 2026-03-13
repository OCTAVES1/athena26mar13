from scapy.all import Ether, ARP, sendp, Padding

print("[*] Initializing Scapy Flood & Strike...")

# 1. The Encryption Engine
def xor_cipher(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

plaintext = b"GHOST_IN_THE_WIRE!"
psk = b"WOLF"
ciphertext = xor_cipher(plaintext, psk)

# 2. Generate the Pre-Strike Noise (50 normal ARP packets)
print("[*] Firing Pre-Strike ARP Flood (50 packets)...")
noise_wave_1 = [Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"10.0.0.{i}") for i in range(10, 60)]
sendp(noise_wave_1, iface="h1-eth0", verbose=False)

# 3. Inject the Encrypted Ghost Frame
print("[*] Injecting Encrypted PadSteg Payload...")
ghost_frame = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="10.0.0.2") / Padding(load=ciphertext)
sendp(ghost_frame, iface="h1-eth0", verbose=False)

# 4. Generate the Post-Strike Noise (50 normal ARP packets)
print("[*] Firing Post-Strike ARP Flood (50 packets)...")
noise_wave_2 = [Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"10.0.0.{i}") for i in range(61, 110)]
sendp(noise_wave_2, iface="h1-eth0", verbose=False)

print("[+] Strike Complete. No errors. Target successfully saturated.")
