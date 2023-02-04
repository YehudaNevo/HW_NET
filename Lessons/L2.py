from scapy.all import *

mac = "dc:a9:04:80:a2:d7"
def filter_mac(frame):
    return (Ether in frame) and (frame[Ether].dst == mac)

frames = sniff(count=20,filter=filter_mac)

for f in frames:
    f.show()