from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from pymongo import Connection
from pymongo.errors import PyMongoError

class MyHandler(BaseHTTPRequestHandler):

    

    def do_PUT(self):

        length = int(self.headers.get("Content-Length"))
        content = self.rfile.read(length)

        try:
            msg = json.loads(content)
            _, project_name, record_label, _ = self.path.split('/') 
            msg['record_label']=record_label
            msg['project_name']=project_name
        except ValueError:
            self.send_response(400, "request badly formatted")
            return
        try:
            connection = Connection()
            db = connection.smtdb 
            simulations = db.simulations
            simulations.insert(msg)
        except PyMongoError:
            self.send_response(500, "could not connect to database")
            return

        self.send_response(200)
        
def main():

    try:
        server = HTTPServer(('', 5000), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

