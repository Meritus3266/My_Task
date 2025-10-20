from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = []

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 202):
         self.send_response(status)
         self.send_header("Content-Type", "application/json")
         self.end_headers()
         self.wfile.write(json.dumps(payload).encode())
    def do_PUT(self):
         content_size = int(self.headers.get("Content-Length", 0))
         parsed_data = self.rfile.read(content_size)
         put_data = json.loads(parsed_data)
         update_name = put_data.get("name")
         for entry in data:
              if entry.get("name") == update_name:
                 entry.update(put_data)
              break
         else: data.append(put_data)
         self.send_data({
              "Message": "update complete",
              "data": put_data
         },status = 202)

def run():
       HTTPServer(('0.0.0.0', 7000), BasicAPI).serve_forever()
print("Application is running!")
run()
