import logging
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)


class Core(CorePluginBase):
    def enable(self):
        log.debug("TorrentFilter Core enabled")

    def disable(self):
        log.debug("TorrentFilter Core disabled")
