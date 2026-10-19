import logging
import deluge.component as component
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)


class Core(CorePluginBase):
    def enable(self):
        log.debug("TrackerStatus Core enabled")
        try:
            core = component.get("Core")
            if hasattr(core, "register_status_field"):
                core.register_status_field("tracker_status", self._get_tracker_status)
        except Exception as e:
            log.debug("Core.register_status_field exception (expected if already built-in): %s", e)

    def disable(self):
        log.debug("TrackerStatus Core disabled")
        try:
            core = component.get("Core")
            if hasattr(core, "deregister_status_field"):
                core.deregister_status_field("tracker_status")
        except Exception as e:
            log.debug("Core.deregister_status_field exception: %s", e)

    def _get_tracker_status(self, torrent_id):
        try:
            torrent_manager = component.get("TorrentManager")
            if torrent_id in torrent_manager.torrents:
                torrent = torrent_manager.torrents[torrent_id]
                return getattr(torrent, "tracker_status", "")
        except Exception:
            pass
        return ""
