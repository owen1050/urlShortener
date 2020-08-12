
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib, ssl, os


host = "http://short.owenbusler.com/"

class urlShortHttpServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global host
        reply = ""
        if(self.path.find("newURL") > 0):

            path = self.path
            path = urllib.parse.unquote(path)

            i0 = path.find("url=") + 4
            i1 = path.find("&")
            url = path[i0:i1]

            i0 = path.find("path=") + 5
            short = path[i0:]

            self.send_response(200)
            self.send_header("content-type", "text/plain")
            self.end_headers()
            
            shorts = self.getUrls()
            if(short in shorts):
                reply = "ALready used, pick a new name"
            else:
                self.addToUrls(url, short)
                reply = "Will now foreward " + host + short + " to " + url

        else:
            path = self.path[1:]

            urls = self.getUrls()
            print(path, urls, path in urls)
            if path in urls:

                self.send_response(301)
                self.send_header("Status", "301 Found")
                self.send_header("Location", urls[path])
                self.end_headers()

                reply = "redireted to " + urls[path]
                print("302 redirect")
            else:
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                f = open("main.html", "r")
                page = f.read()
                f.close()
                reply = page
        print(reply)
        self.wfile.write(reply.encode())

    def addToUrls(self, url, short):
        f = open("database.txt", "r")
        oldDb = f.read()
        f.close()

        newLine = "\n" + short + "|" + url
        newDb = oldDb + newLine

        f = open("database.txt", "w")
        f.write(newDb)
        f.close()

    def getUrls(self):
        f = open("database.txt", "r")
        oldDb = f.read()
        f.close()

        lines = oldDb.split("\n")
        retDict = {}
        for line in lines:
            l = line.split("|")
            retDict[l[0]] = l[1]

        return retDict


server_address = ('',5432)     
httpd = HTTPServer(server_address, urlShortHttpServer)
print('running server...')        
try:         
    httpd.serve_forever()     
except:         
    httpd.shutdown()         
    print("Shutdown server")          
