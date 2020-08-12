
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib, ssl, os


host = "http://owenbusler.com/"

class urlShortHttpServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global host
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

            self.addToUrls(url, short)
            retStr = "Will now foreward " + host + short + " to " + url

            self.wfile.write(retStr.encode())
        else:
            path = self.path[1:]

            urls = self.getUrls()
            print(path, urls, path in urls)
            if path in urls:
                self.send_response(302)
                self.send_header("Location", urls[path])
                self.end_headers()

                self.wfile.write("red".encode())
            else:
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                f = open("main.html", "r")
                page = f.read()
                f.close()
                self.wfile.write(page.encode())

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
dir_path = os.path.dirname(os.path.realpath(__file__))
httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile=dir_path+"/server.key",
        certfile=dir_path+"/server.cert", server_side=True)
print('running server...')        
try:         
    httpd.serve_forever()     
except:         
    httpd.shutdown()         
    print("Shutdown server")          