import os
import json
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
import smtplib
from email.message import EmailMessage

class Handler(SimpleHTTPRequestHandler):

    def do_POST(self):

        # BUY BUTTON (check stock only)
        if self.path == "/buy":

            try:
                with open("stock.json","r") as f:
                    data = json.load(f)
            except:
                data = {"snake":0}

            if data["snake"] > 0:
                self.send_response(200)
            else:
                self.send_response(400)

            self.end_headers()


        # ORDER SUBMIT (reduce stock + email order)
        elif self.path == "/order":

            length = int(self.headers['Content-Length'])
            body = self.rfile.read(length).decode()

            try:
                with open("stock.json","r") as f:
                    data = json.load(f)
            except:
                data = {"snake":0}

            if data["snake"] <= 0:
                self.send_response(400)
                self.end_headers()
                return

            # reduce stock
            data["snake"] -= 1

            with open("stock.json","w") as f:
                json.dump(data,f)

            # generate order id
            order_id = "SNK-" + str(int(time.time()))

            # create email text
            email_text = f"""
New Flexi Snake Order

Order ID: {order_id}

Customer Details:
{body}

Time: {time.ctime()}
"""

            msg = EmailMessage()
            msg["Subject"] = f"Snake Order {order_id}"
            msg["From"] = "flexisnakestore@gmail.com"
            msg["To"] = "flexisnakestore@gmail.com"

            msg.set_content(email_text)

            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com",465)
                server.login("flexisnakestore@gmail.com","ytwx piae jnkw akne ")
                server.send_message(msg)
                server.quit()
            except Exception as e:
                print("Email error:", e)

            self.send_response(200)
            self.end_headers()

        else:
            self.send_error(404)


# Render or local port
port = int(os.environ.get("PORT",8000))

print("Server running on port",port)

HTTPServer(("0.0.0.0",port), Handler).serve_forever()
