from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from pymongo import Connection
from pymongo.errors import PyMongoError
import re

def get(project, label):
    record_obj = db.simulations.find_one(
            {"project_name":project,"record_label":label})
    del record_obj['_id']
    msg = json.dumps(record_obj)
    print msg
    return msg

def list(project):
    def format_url(record):
        return "%s%s/%s" % (server_url, project, record)

    record_objs = db.simulations.find({"project_name":project})

    urls = [format_url(record['record_label']) for record in record_objs]
    msg = json.dumps({"records":urls})
    print msg
    return msg

urlpatterns = [(r'^/(?P<project>.+)/(?P<label>.+)$', get),
               (r'^/(?P<project>.+)/$', list)
              ]

connection = Connection()
db = connection.smtdb 
server_url = "http://127.0.0.1:5000/"

class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self,request, client_address, server)

    def do_GET(self):
        
        for pattern, handler in urlpatterns:
            match = re.match(pattern, self.path)
            if match:
                args = match.groupdict()
                try:
                    out = handler(**args)
                except PyMongoError:
                    self.send_response(500, "could not connect to database")
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(out)
                return

        self.send_response(400,"request badly formatted")
        return


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

