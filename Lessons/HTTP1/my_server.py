from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 9999


class my_server(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1> hello </h1></body></html>", "utf-8"))


server = HTTPServer((HOST, PORT), my_server)
print("server running..")
server.serve_forever()
server.server_close()
print("server stopped")
