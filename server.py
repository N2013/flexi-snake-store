import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

class Handler(SimpleHTTPRequestHandler):

    def do_POST(self):

        if self.path == "/buy":

            with open("stock.json","r") as f:
                data = json.load(f)

            if data["snake"] > 0:
                data["snake"] -= 1

                with open("stock.json","w") as f:
                    json.dump(data,f)

                self.send_response(200)
            else:
                self.send_response(400)

            self.end_headers()

        else:
            self.send_error(404)


port = int(os.environ.get("PORT",8000))

print("Server running on port",port)

HTTPServer(("0.0.0.0",port), Handler).serve_forever()
