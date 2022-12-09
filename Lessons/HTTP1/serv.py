import socket
import re
import sys

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 80

# dictionary of redirection urls
dic_of_redirection_urls = {'/yehuda': '/index.html'}
# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)


# ['GET /<PATH> HTTP/1.1\r', 'User-Agent: <NAME>\r',.....]
def validate_http_request(request):
    headers_1 = request.split("\n")
    h0 = headers_1[0]
    pattern = r'GET\s+\S+\s+HTTP/1\.[0|1]'
    return bool(re.match(pattern, h0))


while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Send HTTP response

    # Parse HTTP headers
    code = "200"
    headers = request.split('\n')
    filename = headers[0].split()[1]
    print("headers: ", headers)
    print("fileName: ", filename)

    # Get the content of the file

    if filename in dic_of_redirection_urls.keys():
        filename = dic_of_redirection_urls[filename]
        code = "302"
    if filename == '/':
        filename = '/index.html'
    try:
        fin = open("webroot" + filename, encoding="utf8", errors='ignore')
        content = fin.read()
        fin.close()
        size = sys.getsizeof(content)
        response = 'HTTP/1.0 ' + code + ' OK\r\n\n'+ content
        print(response[0:30])
    except FileNotFoundError:
        code = "404"
        response = 'HTTP/1.0' + code + ' NOT FOUND\r\n\nFile Not Found'

    valid = validate_http_request(request)
    if valid:
        client_connection.sendall(response.encode())

# Close socket
server_socket.close()
