import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import config
import os
import sys
current_dir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
from urls import *
from datetime import datetime

class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **config.settings)
        print("Init handle successful.........:", datetime.now())

def main():
    start_status = 0
    print(".....Server starting....", datetime.now())
    application = Application()

    if start_status == 0:
        http_server = tornado.httpserver.HTTPServer(application,max_buffer_size=504857600,xheaders=True)
        http_server.listen(config.listen_port)

        print(
            '''
            "************************************"\n
            ".....Server startup successful...."\n
            "http://localhost:{:0}"\n
            "************************************"\n
            '''.format(config.listen_port)
        )
        tornado.ioloop.IOLoop.current().start()
    else:
        print(
            '''
            "===================================="
            ".....Server startup failure...."
            "===================================="
            '''
        )

if __name__ == "__main__":


    main()

