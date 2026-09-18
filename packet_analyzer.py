from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime


packet_count = 0
tcp_count = 0
udp_count = 0
icmp_count = 0
other_count = 0


def analyze_packet(packet):
    global packet_count
    global tcp_count
    global udp_count
    global icmp_count
    global other_count

    packet_count += 1

    print("\n" + "=" * 60)
    print(f"PACKET #{packet_count}")
    print("=" * 60)

    print("Time:", datetime.now().strftime("%H:%M:%S"))

    if IP in packet:
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        print("Source IP:", source_ip)
        print("Destination IP:", destination_ip)

        if TCP in packet:
            protocol = "TCP"
            tcp_count += 1

        elif UDP in packet:
            protocol = "UDP"
            udp_count += 1

        elif ICMP in packet:
            protocol = "ICMP"
            icmp_count += 1

        else:
            protocol = "Other IP"
            other_count += 1

        print("Protocol:", protocol)
        print("Packet Length:", len(packet), "bytes")

    else:
        other_count += 1
        print("Protocol: Non-IP")
        print("Packet Length:", len(packet), "bytes")


print("=" * 60)
print("             NETWORK PACKET ANALYZER")
print("=" * 60)
print()
print("[+] Packet capture started")
print("[+] Press CTRL+C to stop")
print()

try:
    sniff(
    prn=analyze_packet,
    count=50,
    store=False
)
    

except KeyboardInterrupt:
    print("\n[!] Packet capture stopped by user.")

finally:
    print("\n")
    print("=" * 60)
    print("                 CAPTURE SUMMARY")
    print("=" * 60)

    print(f"Total Packets : {packet_count}")
    print(f"TCP Packets   : {tcp_count}")
    print(f"UDP Packets   : {udp_count}")
    print(f"ICMP Packets  : {icmp_count}")
    print(f"Other Packets : {other_count}")

    print("=" * 60)
    print("           PACKET CAPTURE COMPLETE")
    print("=" * 60)