#!/usr/bin python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from working_with_crud.database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi
import re

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.hello_get()
                return

            if self.path.endswith("/hola"):
                self.hola_get()
                return

            if self.path.endswith("/restaurants"):
                self.restaurants_get()
                return

            if self.path.endswith("/restaurants/new"):
                self.restaurants_new_get()
                return

            p = re.compile('/restaurants/(\d+)/edit$')
            m = p.search(self.path)
            if (m):
                id = m.group(1)
                print("RestaurantID: {}".format(m.group(1)))
                self.restaurants_edit_get(id)
                return

            p = re.compile('/restaurants/(\d+)/delete$')
            m = p.search(self.path)
            if (m):
                id = m.group(1)
                print("RestaurantID: {}".format(m.group(1)))
                self.restaurants_delete_get(id)
                return

        except IOError:
                self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                self.hello_post()

            if self.path.endswith("/restaurants/new"):
                self.restaurants_new_post()
                return


            p = re.compile('/restaurants/(\d+)/edit$')
            m = p.search(self.path)
            if (m):
                id = m.group(1)
                print("RestaurantID: {}".format(m.group(1)))
                self.restaurants_edit_post(id)
                return

            p = re.compile('/restaurants/(\d+)/delete$')
            m = p.search(self.path)
            if (m):
                id = m.group(1)
                print("RestaurantID: {}".format(m.group(1)))
                self.restaurants_delete_post(id)
                return

        except Exception as e:
                print(e)

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
        self.wfile.write(output.encode())
        print(output)
        return

    def restaurants_get(self):
        restaurants = session.query(Restaurant).all()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = "<html><body>"
        output += "<h1>Restaurants</h1>"
        output += "<h2><a href='restaurants/new'>Make a New Restaurant</a><br></h2>"
        for r in restaurants:
            print(r)

            output += r.name + '<br>'
            url = "/restaurants/{}".format(r.id)
            output += "<a href='{}/edit'>Edit</a><br>".format(url)
            output += "<a href='{}/delete'>Delete</a><br><br>".format(url)
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return

    def restaurants_new_get(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ''
        output += '<html><body>'
        output += '<h1>Make a New Restaurant</h1>'
        output += '<form  enctype="multipart/form-data" action="/restaurants/new" method="POST">'
        output += '<input type="text" name="name" id="name" placeholder="Restaurant Name">'
        output += '<input type="submit" value="Create">'
        output += "</form>"
        output += "</html></body>"
        self.wfile.write(output.encode())
        print(output)
        return

    def restaurants_new_post(self):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header("Location","/restaurants")
        self.end_headers()

        form_resp = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        name = form_resp.getvalue("name", '{no name}')

        r = Restaurant(name=name)
        session.add(r)
        session.commit()
        print('New restaurant: {}'.format(name))
        return

    def restaurants_edit_get(self, id):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        r = session.query(Restaurant).filter_by(id=id).first()

        output = ''
        output += '<html><body>'
        output += '<h1>{}</h1>'.format(r.name)
        output += '<form  enctype="multipart/form-data" action="/restaurants/{}/edit" method="POST">'.format(id)
        output += '<input type="text" name="name" id="name" placeholder="Restaurant Name">'
        output += '<input type="submit" value="Rename">'
        output += "</form>"
        output += "</html></body>"
        self.wfile.write(output.encode())
        print(output)
        return

    def restaurants_edit_post(self, id):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header("Location","/restaurants")
        self.end_headers()

        r = session.query(Restaurant).filter_by(id=id).first()

        form_resp = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        name = form_resp.getvalue("name", '{no name}')

        r.name = name
        session.add(r)
        session.commit()
        print('New restaurant name: {}'.format(name))
        return

    def restaurants_delete_get(self, id):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        r = session.query(Restaurant).filter_by(id=id).first()

        output = ''
        output += '<html><body>'
        output += '<h1>Are you sure you want to delete {}?</h1>'.format(r.name)
        output += '<form  enctype="multipart/form-data" action="/restaurants/{}/delete" method="POST">'.format(id)
        output += '<input type="submit" value="Delete">'
        output += "</form>"
        output += "</html></body>"
        self.wfile.write(output.encode())
        print(output)
        return

    def restaurants_delete_post(self, id):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header("Location","/restaurants")
        self.end_headers()

        r = session.query(Restaurant).filter_by(id=id).first()

        session.delete(r)
        session.commit()
        print('{} deleted'.format(r.name))
        return

    def hello_post(self):
        self.send_response(301)
        self.end_headers()
        # ctype, pdict = cgi.parse_header(self.headers['content-type'])
        # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        # if ctype == 'multipart/form-data':
        #     fields = cgi.parse_multipart(self.rfile, pdict)
        #     messagecontent = fields["message"][0].decode()

        form_resp = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})
        messagecontent = form_resp.getvalue("message", '{no message}')

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
        server = HTTPServer(('', port), WebserverHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
