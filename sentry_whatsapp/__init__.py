import time
import base64
from Yowsup.connectionmanager import YowsupConnectionManager


try:
    VERSION = __import__('pkg_resources') \
        .get_distribution(__name__).version
except Exception, e:
    VERSION = 'unknown'


class WhatsappSender(object):
    """Send Whatsapp messages.

    based on http://goo.gl/qUB7N
    """

    def __init__(self, login, password):
        connectionManager = YowsupConnectionManager()
        self.signals = connectionManager.getSignalsInterface()
        self.methods = connectionManager.getMethodsInterface()
        self.signals.registerListener("auth_success", self.onAuthSuccess)
        self.signals.registerListener("auth_fail", self.onAuthFailed)
        self.login = login
        self.password = base64.b64decode(bytes(password.encode('utf-8')))
        self.done = False

    def send(self, phone, message):
        if '-' in phone:
            self.jid = "%s@g.us" % phone
        else:
            self.jid = "%s@s.whatsapp.net" % phone
        self.message = message
        self.methods.call("auth_login", (self.login, self.password))
        while not self.done:
            time.sleep(0.5)
        print("WA: Done.")

    def onAuthSuccess(self, username):
        self.methods.call("message_send", (self.jid, self.message))
        self.done = True
        print("WA: Sent!")

    def onAuthFailed(self, username, err):
        print("Auth Failed!")
