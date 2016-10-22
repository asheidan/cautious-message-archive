import sys
import os

from . import settings

__version__ = "0.0.0"


run_as_application = getattr(sys, "frozen", False)

if run_as_application:
    resource_dir = os.path.realpath(os.path.dirname(__file__))
    base_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__),
                     "..", "..", "..", "..", "..")
    )
else:
    resource_dir = os.path.realpath(os.path.join(
        os.path.dirname(__file__), "frontend", "dist"
    ))
    base_dir = os.path.realpath(os.path.dirname(__file__))
