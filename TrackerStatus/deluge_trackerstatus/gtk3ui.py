import logging
import deluge.component as component
from deluge.plugins.pluginbase import Gtk3PluginBase

log = logging.getLogger(__name__)

try:
    _
except NameError:
    _ = lambda s: s

COLUMN_TITLE = "Tracker Status"


class Gtk3UI(Gtk3PluginBase):
    def __init__(self, plugin_name):
        super(Gtk3UI, self).__init__(plugin_name)
        self.column_name = _(COLUMN_TITLE)

    def enable(self):
        log.debug("TrackerStatus Gtk3UI enabled")
        self.torrentview = component.get("TorrentView")
        self.add_column()

    def disable(self):
        log.debug("TrackerStatus Gtk3UI disabled")
        self.remove_column()

    def add_column(self):
        if not hasattr(self, "torrentview") or self.torrentview is None:
            return

        if self.column_name not in self.torrentview.columns:
            self.torrentview.add_text_column(
                self.column_name,
                status_field=["tracker_status"],
                default=True,
                hidden=False,
            )

    def remove_column(self):
        if not hasattr(self, "torrentview") or self.torrentview is None:
            return

        if self.column_name in self.torrentview.columns:
            self.torrentview.remove_column(self.column_name)
        elif COLUMN_TITLE in self.torrentview.columns:
            self.torrentview.remove_column(COLUMN_TITLE)
