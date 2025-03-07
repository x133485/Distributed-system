import http.server
import json
import socketserver

courses = ["Database system", "Mathematics", "Distributed System", "Computer Network"]

class RESTRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  
        self.send_header('Content-type', 'application/json')  
        self.end_headers()  
        self.wfile.write(json.dumps(courses).encode())  # 发送 JSON 数据

# Set the server's port
port = 8080
httpd = socketserver.TCPServer(("", port), RESTRequestHandler)

print(f"REST Services running on port {port}")
httpd.serve_forever()
