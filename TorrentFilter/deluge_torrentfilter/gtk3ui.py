import logging
import deluge.component as component
from deluge.plugins.pluginbase import Gtk3PluginBase

log = logging.getLogger(__name__)


class Gtk3UI(Gtk3PluginBase):
    def enable(self):
        log.debug("TorrentFilter Gtk3UI enabled")
        try:
            from gi.repository import Gtk
            toolbar_comp = component.get("ToolBar")
            if hasattr(toolbar_comp, "toolbar"):
                self.tool_item = Gtk.ToolItem()
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
                
                label = Gtk.Label(label="Filter:")
                box.pack_start(label, False, False, 2)
                
                self.search_entry = Gtk.SearchEntry()
                self.search_entry.set_placeholder_text("Filter by name...")
                self.search_entry.set_width_chars(22)
                self.search_entry.connect("search-changed", self._on_search_changed)
                box.pack_start(self.search_entry, False, False, 0)
                
                self.tool_item.add(box)
                self.tool_item.show_all()
                toolbar_comp.toolbar.insert(self.tool_item, -1)
        except Exception as e:
            log.debug("Gtk3UI enable exception: %s", e)

    def disable(self):
        log.debug("TorrentFilter Gtk3UI disabled")
        try:
            if hasattr(self, "tool_item"):
                toolbar_comp = component.get("ToolBar")
                if hasattr(toolbar_comp, "toolbar"):
                    toolbar_comp.toolbar.remove(self.tool_item)
            tv = component.get("TorrentView")
            if hasattr(tv, "set_filter") and hasattr(tv, "filter") and tv.filter:
                filter_dict = dict(tv.filter)
                filter_dict.pop("name", None)
                tv.set_filter(filter_dict)
        except Exception as e:
            log.debug("Gtk3UI disable exception: %s", e)

    def _on_search_changed(self, entry):
        text = entry.get_text().strip()
        try:
            tv = component.get("TorrentView")
            if hasattr(tv, "set_filter"):
                filter_dict = dict(tv.filter) if tv.filter else {}
                if text:
                    filter_dict["name"] = text
                else:
                    filter_dict.pop("name", None)
                tv.set_filter(filter_dict)
        except Exception as e:
            log.debug("_on_search_changed exception: %s", e)
