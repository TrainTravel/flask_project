#! /usr/bin/env python
#import sys
#print(sys.path)
from gevent.pywsgi import WSGIServer
from manage import application, manager

#http_server = WSGIServer(('', 8000), application)
#http_server.serve_forever()
#manager.run()
if __name__ == "__main__":
    application.run(threaded=True)
    manager.run()
    print('hi app')
