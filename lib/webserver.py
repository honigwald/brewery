import SimpleHTTPServer
import SocketServer

Port = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", Port), Handler)

print "serving at port", Port

httpd.serve_forever()
