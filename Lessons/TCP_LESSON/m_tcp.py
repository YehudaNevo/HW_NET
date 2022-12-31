from scapy.all import *

packets = rdpcap("SYNflood.pcapng")
packet_counts = {}
ip_list = ['185.39.11.29', '185.39.10.95', '185.39.10.58', '193.27.228.146', '185.39.10.29', '185.39.11.111',
           '185.39.10.52', '185.153.197.104', '195.54.166.101', '31.10.5.89', '195.54.167.140', '185.39.10.27',
           '185.39.11.88', '195.54.167.144', '185.39.10.19', '79.124.62.18', '185.153.197.11', '92.63.196.3',
           '118.184.168.26', '194.26.29.31', '185.153.197.101', '45.134.179.57', '193.27.228.147', '2.92.254.38',
           '185.153.197.103', '193.27.228.145', '195.54.161.26', '185.156.73.38', '194.26.29.52', '156.96.156.136',
           '185.39.11.47', '194.26.29.53', '45.148.10.184', '185.176.27.14', '51.91.212.81', '213.217.1.225',
           '193.27.228.148', '171.67.71.100', '103.84.178.98', '195.54.167.141', '195.54.166.143', '188.129.232.167',
           '36.89.128.251', '193.27.228.135', '194.26.29.25', '185.53.88.240', '45.141.84.44', '94.102.51.17',
           '185.23.214.140', '45.92.126.74', '195.54.160.60']

ips_dict = {}
start_time = packets[1].time
end_time = packets[-1].time
time = round(end_time - start_time,1)



for p in packets:
    if p.haslayer(IP):
        if p[IP].src not in ips_dict.keys():  # new ip
            ips_dict[p[IP].src] = 0
        ips_dict[p[IP].src] += 1

ips_ratio_pac_per_time = sorted ([[ip,  int(ips_dict[ip] // time )] for ip in ips_dict.keys()], key=lambda x: x[1], reverse=True)
print(ips_ratio_pac_per_time)
print(len(ips_ratio_pac_per_time))

x =  [e for e in ips_ratio_pac_per_time[:200]]
print(x[-1])
x =  [e[0] for e in ips_ratio_pac_per_time[:200]]
s = set(ip_list)
print(len(s.intersection(x)))

