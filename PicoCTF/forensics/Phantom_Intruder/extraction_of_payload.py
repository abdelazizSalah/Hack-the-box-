from scapy.all import rdpcap, TCP, Raw
import base64

packets = rdpcap("Phantom_Intruder.pcap")

for i, pkt in enumerate(packets):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        data = bytes(pkt[Raw].load)
        if len(data) >= 12:
            last12 = data[-12:]
            try:
                decoded = base64.b64decode(last12).decode(errors="ignore")
            except Exception:
                decoded = "(invalid base64)"
            print(f"Packet {i}: {last12.hex()} -> {decoded}")
