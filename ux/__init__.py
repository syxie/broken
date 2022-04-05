# Other library imports
# import requests
# from json import dumps

# Project imports
# from settings import settings
import util
import ux.irc

class UX(object):
    """
    Class to manage calls to various user interfaces.
    """

    def __init__(self):
        super().__init__()
        self.irc = ux.irc.bot()

    def __xmerged__(self):
        """
        Called when xmerge has been completed in the webapp.
        Merge all instances into child classes.
        """
        init_map = {
            "ux": self,
            "sinks": self.sinks,
            "webapp": self.webapp,
            "irc": self.irc,
        }
        util.xmerge_attrs(init_map)
        #init_map["irc"].__xmerged__()
