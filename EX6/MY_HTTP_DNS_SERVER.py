import socket
from string import Template
from scapy import *
from scapy.all import DNS, DNSQR, IP, sr1, UDP

MY_IP = '0.0.0.0'
DNS_SERVER = "8.8.8.8"
MY_PORT = 8153
SOCKET_TIMEOUT = 3
FIXED_RESPONSE = ""


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


def domain_to_ip(domain):
    # Build the DNS query packet
    packet = IP(dst=DNS_SERVER) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))

    # Send the packet and get the response
    response = sr1(packet, verbose=0)

    res = []
    size = response.ancount

    for i in range(0, size):
        if response.an[i].type == 1:
            res.append(response.an[i].rdata)

    return create_nice_html(res, "List of IPs:")


def ip_to_domains(ip):
    r_ip = reverse_ip(ip)
    # Build the DNS query packet
    packet = IP(dst=DNS_SERVER) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=r_ip, qtype="PTR"))

    # Send the packet and get the response
    try:
        response = sr1(packet, verbose=0)
    except:
        response = ""
    # response.show()
    res = []
    size = response.ancount
    # response.show()
    for i in range(size):
        if response.an[i].type == 12:  # ptr req..
            res.append(response.an[i].rdata.decode())
    return create_nice_html(res, "List of hosts names:")


def create_nice_html(arr, name):
    lst_template = Template("<li>  $ele </li>")
    ele_arr = "".join([lst_template.substitute(ele=ele) for ele in arr])
    template_html = Template("""
    <html>
    <head> 
    <style>  
     body{
     background-color: rgb(248, 236, 209);
                }           

            ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
      }

      /* Define a style for each list item */
      li {
        list-style-type: circle;
        padding: 10px;
        margin-bottom: 10px;
        background-color: rgb(222, 182, 171);
      }
    </style>
  </head>
  <body>
    <h1>$name</h1>
    <ul>
    $loop_element
        </ul>
        </body>
        </html>""")
    return template_html.substitute(loop_element=ele_arr, name=name)


#  send the content encoded  to client
def handle_client_request(resource, client_socket):
    if resource == '/':
        response = ('HTTP/1.0 200 OK\n\n please enter url').encode()

    elif re.match(r"www\.(\w+\.\w+)(\.\w+)?(\/\w+)*", resource):
        result_ips = domain_to_ip(resource)
        response = ('HTTP/1.0 200 OK\n\n' + result_ips).encode()

    elif re.match("^reverse\/+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", resource):
        result_domains_name = ip_to_domains(resource[8:])
        response = ('HTTP/1.0 200 OK\n\n' + result_domains_name).encode()
    else:
        response = ('HTTP/1.0 200 OK\n\nplease enter valid url, you send: ' + resource).encode()
    client_socket.send(response)


def handle_client(client_socket):
    while True:
        # Get the client request
        request = client_socket.recv(1024).decode()
        headers = request.split("\n")
        h0 = headers[0]
        idx_end_of_resource = h0.find("HTTP") - 1
        resource = h0[5:idx_end_of_resource]
        handle_client_request(resource, client_socket)
        break
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((MY_IP, MY_PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(MY_PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
