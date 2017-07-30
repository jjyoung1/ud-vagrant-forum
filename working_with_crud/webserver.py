from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.hello_get()
                return

            if self.path.endswith("/hola"):
                self.hola_get()
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def hola_get(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "&#161Hola!"
        output += "<br><a href='/hello'>Back to Hello</a"
        output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                          <h2>What would you like me to say?</h2>
                          <input name='message' type='text'>
                          <input type='submit' value='Submit'></form>"""
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)

    def hello_get(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>" \
                  "Hello!"
        output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                          <h2>What would you like me to say?</h2>
                          <input name='message' type='text'>
                          <input type='submit' value='Submit'></form>"""
        output += "</body></html>"
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return

    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                self.hello_post()

        except Exception as e:
            print(e)

    def hello_post(self):
        self.send_response(301)
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields["message"][0].decode()

        # length = int(self.headers.get('Content-Length', 0))
        # data = self.rfile.read(length).decode()
        # params = parse_qs(data)
        # messagecontent = params['message'][0]
        output = ""
        output += "<html><body>"
        output += "<h2> Okay, how about this: </h2>"
        output += "<h1> {} </h1>".format(messagecontent)
        output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                          <h2>What would you like me to say?</h2>
                          <input name='message' type='text'>
                          <input type='submit' value='Submit'></form>"""
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
