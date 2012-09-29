from config import PORT

from brubeck.request_handling import Brubeck
from brubeck.connections import WSGIConnection
from brubeck.request_handling import WebMessageHandler

import gevent
import time

class WaitHandler(WebMessageHandler):

    def get(self):
        """
        Do some "work" OAuthing.  Return.
        """
        start = time.time()
        ms = float(self.get_argument('ms', 1000))
        gevent.sleep(ms / 1000)

        duration = time.time() - start
        self.set_body("<p>Requested %s</p><p>Actual: %s</p>" % (
            str(ms), str(duration * 1000)))
        return self.render()


app = Brubeck(**{
    'msg_conn': WSGIConnection(port=PORT),
    'handler_tuples': [
        (r'^/wait/?$', WaitHandler),
    ]
})

def application(environ, callback):
    return app.msg_conn.process_message(app, environ, callback)
