#! /usr/bin/env python3

from scapy.all import DNS, DNSQR,DNSRR, IP, sr1, UDP

# dns_req = IP(dst='8.8.8.8') / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qtype="PTR", qname="216.58.211.206"))
# res = sr1(dns_req)
# print(res[DNS].show())


# answer = sr1(dns_req)

# print(answer[DNS].show())


def reverse_ip(ip):
    # Split the IP address into a list of octets
    octets = ip.split('.')

    # Reverse the list of octets
    octets.reverse()

    # Join the octets into a reversed IP string
    reversed_ip = '.'.join(octets)

    # Append ".in-addr.arpa" to the reversed IP
    reversed_ip += '.in-addr.arpa'

    return reversed_ip


from scapy.all import *
def ip_to_domains(ip):
    # Set the DNS server to use
    dns_server = "8.8.8.8"
    r_ip = reverse_ip(ip)
    # Build the DNS query packet
    packet = IP(dst=dns_server) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=r_ip,qtype="PTR"))

    # Send the packet and get the response
    try:
        response = sr1(packet, verbose=0)
    except:
        response = ""
    # response.show()
    response.show()
    res = []
    size = response.ancount
    # response.show()
    for i in range(0, size):
        if response.an[i].type == 12:
            res.append(response.an[i].rdata.decode())
    print(res)



#packet = IP(dst='google.com') / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com"))

#print(packet.dst)

# ip_to_domains("216.58.205.206")
ip_to_domains("216.58.205.206")




#for i in range(len(response.an)) :
 #   print(response.an[i])
# x = response[DNS].an
# print((x.rdata))

#x.show()
# def ip_to_domains(ip):
#     dns_server = "8.8.8.8"
#     # Build the DNS query packet
#     packet = IP(dst=dns_server) / UDP(dport=53) / DNS(rd=1, an=DNSRR(rdata=ip))
#
#     # Send the packet and get the response
#     response = sr1(packet, verbose=0)
#     res = []
#     # Print the IPs of the domain
#     for ele in response[DNS].an:
#         res.append(ele.rdata)
#     return create_nice_html(res, "List of IPs:")

#
# def generate_html_template(title, content):
#     html_template = f"""
#     <html>
#         <head>
#             <title>{title}</title>
#         </head>
#         <body>
#             {content}
#         </body>
#     </html>
#     """
#     return html_template


#
# import scapy.all as scapy
#
# def get_domain(ip):
#     try:
#         ans, unans = scapy.sr(scapy.DNSQR(qname=ip))
#         for s, r in ans:
#             return r.rrname
#     except Exception as e:
#         print(e)
#         return None
#
# print(get_domain( "172.217.16.132"))
