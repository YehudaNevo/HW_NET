from scapy.all import *

"""
To identify suspicious IP addresses, the following criteria were used:

High packet rate:
Sources that send a large number of packets per second were considered suspicious.
This could be an indication of a denial of service (DoS) attack or other malicious activity.

Wide range of destination addresses:
Sources that send packets to a wide range of destination addresses were also
considered suspicious.
This could indicate that the source is attempting to scan for vulnerable systems or attempting to spread malware to
multiple targets.

SYN packets without ACK packets:
Finally, sources that send a large number of SYN packets
(used to initiate a connection) but no ACK packets (used to acknowledge receipt of the SYN packet)
were considered particularly suspicious. This could indicate an attempt to establish a large number of connections
 without completing the handshake process, which could be a sign of an attempted SYN flood attack.
 """


# this method return ips who send more or eq 2 pack per sec
def ips_who_send_more_then_2_pack_per_sec(packets):
    ips_dict = {}
    start_time = packets[1].time
    end_time = packets[-1].time
    time = round(end_time - start_time, 1)

    for p in packets:
        if p.haslayer(IP):
            if p[IP].src not in ips_dict.keys():  # new ip
                ips_dict[p[IP].src] = 0
            ips_dict[p[IP].src] += 1

    ips_ratio_pac_per_time = sorted([[ip, int(ips_dict[ip] // time)] for ip in ips_dict.keys()], key=lambda x: x[1],
                                    reverse=True)
    res = [ele[0] for ele in ips_ratio_pac_per_time if ele[1] >= 2]
    return set(res)


# this method return the ips who send to many dst  ( more or eq to 10 dst)
def ips_who_send_to_many_dst(packets):
    ips_dict = {}

    for p in packets:
        if p.haslayer(IP):
            if p[IP].src not in ips_dict.keys():  # new ip
                ips_dict[p[IP].src] = set()  # set for all the ips dst from that src ip
            ips_dict[p[IP].src].add(p[IP].dst)

    ips_and_count_dst = sorted([[ip, len(ips_dict[ip])] for ip in ips_dict.keys()], key=lambda x: x[1], reverse=True)

    ips = [ip[0] for ip in ips_and_count_dst if ip[1] >= 10]
    return set(ips)


# this method wll return the ips who sand the most syn packets ( more or eq to 10, BUT 0 ack )
def syn_but_not_ack(packets):
    packet_counts = {}

    class PacketCounter:
        def __init__(self):
            self.syn_count = 0
            self.syn_ack_count = 0
            self.ack_count = 0

        def add_packet(self, packet_type):
            if packet_type == "syn":
                self.syn_count += 1
            elif packet_type == "syn+ack":
                self.syn_ack_count += 1
            elif packet_type == "ack":
                self.ack_count += 1

        def to_dict(self):
            return {
                "syn_count": self.syn_count,
                "syn_ack_count": self.syn_ack_count,
                "ack_count": self.ack_count,
            }

    def add_packet(ip, packet_type):
        if ip in packet_counts:
            packet_counts[ip].add_packet(packet_type)
        else:
            packet_counts[ip] = PacketCounter()
            packet_counts[ip].add_packet(packet_type)

    for p in packets:
        if p.haslayer(TCP):
            if p[TCP].flags == 2:
                add_packet(p[IP].src, 'syn')
            elif p[TCP].flags == 16:
                add_packet(p[IP].src, 'ack')
            elif p[TCP].flags == 18:
                add_packet(p[IP].src, 'syn+ack')

    # print(json.dumps({ip: pc.to_dict() for ip, pc in packet_counts.items()}, indent=2))
    lst = []
    for k, v in packet_counts.items():
        lst.append([k, v.to_dict()])

    lst = sorted(lst, key=lambda x: x[1]["syn_count"], reverse=True)
    # 10 + syn, but not ack
    syn_gt_10_and_ack_eq_0 = [ele[0] for ele in lst if
                              ele[1]['syn_count'] >= 10 and ele[1]['ack_count'] == 0 and ele[1]['syn_ack_count'] == 0]

    return set(syn_gt_10_and_ack_eq_0)


if __name__ == "__main__":
    packets = rdpcap("SYNflood.pcapng")

    x = ips_who_send_more_then_2_pack_per_sec(packets)
    y = ips_who_send_to_many_dst(packets)
    z = syn_but_not_ack(packets)

    Suspicious_IP_addresses = (x.intersection(y).intersection(z))

    # Open the file in write mode
    file = open('HW_RESULT.txt', 'w')

    # Convert the set to a string and write it to the file
    set_str = str(Suspicious_IP_addresses)
    file.write(set_str)

    # Close the file
    file.close()
