# My version with an attempt to FieldStorage
#
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart, FieldStorage
from urllib.parse import parse_qs

form = '''
<form method='POST' enctype='multipart/form-data' action='/hello'>
                      <h2>What would you like me to say?</h2>
                      <input name='message' type='text'>
                      <input type='submit' value='Submit'></form>
'''


class webserverHandler(BaseHTTPRequestHandler):
    def hello_get(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ""
        output += "<html><body>" \
                  "Hello!"
        output += form
        output += "</body></html>"

        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return

    def hello_post(self):
        self.send_response(301)
        self.end_headers()
        formResp = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        message = formResp.getvalue("message", '{no message}')

        output = ""
        output += "<html><body>"
        output += "<h2> Okay, how about this: </h2>"
        output += "<h1> {} </h1>".format(message)

        output += form
        output += "</body></html>"

        self.wfile.write(output.encode())
        print(output)

        return

    def hola_get(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ""
        output += "<html><body>"
        output += "&#161Hola!"
        output += "<br><a href='/hello'>Back to Hello</a"
        output += form
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return

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


    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                self.hello_post()
            return

        except Exception as e:
            print(e)


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
