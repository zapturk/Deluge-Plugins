from deluge.plugins.init import PluginInitBase


class CorePlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .core import Core as PluginClass
        self._plugin_cls = PluginClass
        super(CorePlugin, self).__init__(plugin_name)


class Gtk3UIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .gtk3ui import Gtk3UI as PluginClass
        self._plugin_cls = PluginClass
        super(Gtk3UIPlugin, self).__init__(plugin_name)


class GtkUIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        try:
            from .gtkui import GtkUI as PluginClass
        except ImportError:
            from .gtk3ui import Gtk3UI as PluginClass
        self._plugin_cls = PluginClass
        super(GtkUIPlugin, self).__init__(plugin_name)


class WebUIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .webui import WebUI as PluginClass
        self._plugin_cls = PluginClass
        super(WebUIPlugin, self).__init__(plugin_name)
