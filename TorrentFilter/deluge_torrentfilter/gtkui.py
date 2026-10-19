import logging
import deluge.component as component
from deluge.plugins.pluginbase import GtkUIPluginBase

log = logging.getLogger(__name__)


class GtkUI(GtkUIPluginBase):
    def enable(self):
        log.debug("TorrentFilter GtkUI enabled")

    def disable(self):
        log.debug("TorrentFilter GtkUI disabled")
