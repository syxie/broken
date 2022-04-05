import sinks.fidor
import util


class Sinks(util.Base):
    """
    Class to manage calls to various sinks.
    """

    def __init__(self):
        super().__init__()
        self.account_info = {}

    def __irc_started__(self):
        self.startup()

    def startup(self):
        """
        We NEED the other libraries, and we initialise fast, so don't make
        any race conditions by relying on something that might not be there.
        """
        self.fidor = sinks.fidor.Fidor()
        # setattr(self.truelayer, "sinks", self)

