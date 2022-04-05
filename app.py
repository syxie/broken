#!/usr/bin/env python3
# Twisted/Klein imports
from twisted.internet import reactor
from klein import Klein

# Project imports
import util

# New style classes
import sinks
import ux

init_map = None

class WebApp(util.Base):
    """
    Our Klein webapp.
    """
    app = Klein()

if __name__ == "__main__":
    init_map = {
        "ux": ux.UX(),
        "sinks": sinks.Sinks(),
        "webapp": WebApp(),
    }
    # Merge all classes into each other
    util.xmerge_attrs(init_map)

    # Let the classes know they have been merged
    for class_name, class_instance in init_map.items():
        if hasattr(class_instance, "__xmerged__"):
            class_instance.__xmerged__()

    # Set up the loops to put data in ES
    #init_map["tx"].setup_loops()

    # Run the WebApp
    init_map["webapp"].app.run("127.0.0.1", 8080)
