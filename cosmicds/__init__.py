# Licensed under a 3-clause BSD style license - see LICENSE.rst

from .version import __version__
import sys
import logging

__all__ = []

log = logging.getLogger()

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

from .tools import *

discovered_plugins = entry_points(group='cosmicds.plugins')

STORY_PATHS = {}

for ep in discovered_plugins:
    ep.load()
    log.info("Discovered the `%s` data story.", ep.name)

