# Other library imports
from httpx import ReadTimeout, ReadError, RemoteProtocolError
from datetime import datetime
import logging

log = logging.getLogger("util")


# Color definitions
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = {"WARNING": YELLOW, "INFO": WHITE, "DEBUG": BLUE, "CRITICAL": YELLOW, "ERROR": RED}
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

def get_logger(name):

    # Define the logging format
    FORMAT = "%(asctime)s %(levelname)18s $BOLD%(name)13s$RESET  - %(message)s"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    color_formatter = ColoredFormatter(COLOR_FORMAT)
    # formatter = logging.Formatter(

    # Why is this so complicated?
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # ch.setFormatter(formatter)
    ch.setFormatter(color_formatter)

    # Define the logger on the base class
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Add the handler and stop it being silly and printing everything twice
    log.addHandler(ch)
    log.propagate = False
    return log

class Base(object):
    def __init__(self):
        name = self.__class__.__name__
        # Set up all the logging stuff
        self.log = get_logger(name)
        self.log.info("Class initialised")

def xmerge_attrs(init_map):
    """
    Given a dictionary of strings and classes, set all corresponding class.<string> attributes
    on each class, to every other class.
    "a": A(), "b": B() -> A.b = B_instance, B.a = A_instance
    :param init_map: dict of class names to classes
    """
    for classname, object_instance in init_map.items():
        # notify, Notify
        for classname_inside, object_instance_inside in init_map.items():
            if not classname == classname_inside:
                # irc, bot
                setattr(object_instance, classname_inside, object_instance_inside)