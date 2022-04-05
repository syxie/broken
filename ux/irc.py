# Twisted/Klein imports
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor, ssl
from twisted.internet.task import deferLater

# Project imports
import util

class IRCBot(irc.IRCClient):
    def __init__(self, log):
        """
        Initialise IRC bot.
        :param log: logger instance
        :type log: Logger
        """
        self.log = log
        self.nickname = "testuser1"
        self.realname = self.nickname
        self.username = self.nickname

    def signedOn(self):
        """
        Called when we have signed on to IRC.
        Join our channel.
        """
        self.log.info(f"Signed on as {self.nickname}")
        self.sinks.__irc_started__()

class IRCBotFactory(protocol.ClientFactory):
    def __init__(self):
        self.log = util.get_logger("IRC")
        self.log.info("Class initialised")

    def buildProtocol(self, addr):
        """
        Custom override for the Twisted buildProtocol so we can access the Protocol instance.
        Passes through the Agora instance to IRC.
        :return: IRCBot Protocol instance
        """
        # Pass through the logger
        prcol = IRCBot(self.log)
        self.client = prcol
        setattr(self.client, "sinks", self.sinks)
        setattr(self.client, "ux", self.ux)
        return prcol

def bot():
    factory = IRCBotFactory()
    reactor.connectTCP("irc.freenode.net", 6667, factory)
    return factory
