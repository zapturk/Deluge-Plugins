import logging
from deluge.plugins.pluginbase import WebPluginBase
from .common import get_resource

log = logging.getLogger(__name__)


class WebUI(WebPluginBase):
    scripts = [get_resource('torrentfilter.js')]
    debug_scripts = scripts

    def enable(self):
        log.debug("TorrentFilter WebUI enabled")

    def disable(self):
        log.debug("TorrentFilter WebUI disabled")
