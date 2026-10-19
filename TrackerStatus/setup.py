from setuptools import find_packages, setup

__plugin_name__ = 'TrackerStatus'
__author__ = 'zapturk'
__author_email__ = 'zapturk@users.noreply.github.com'
__version__ = '0.1'
__url__ = 'https://github.com/deluge-torrent/deluge'
__license__ = 'GPLv3'
__description__ = 'Adds Tracker Status column to Deluge torrent list'
__long_description__ = """Adds a Tracker Status column to Deluge torrent list table in GTK UI and Web UI."""
__pkg_data__ = {'deluge_' + __plugin_name__.lower(): ['data/*']}

setup(
    name=__plugin_name__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    long_description=__long_description__,
    packages=find_packages(),
    package_data=__pkg_data__,
    entry_points={
        'deluge.plugin.core': [
            'TrackerStatus = deluge_trackerstatus:CorePlugin',
        ],
        'deluge.plugin.gtk3ui': [
            'TrackerStatus = deluge_trackerstatus:Gtk3UIPlugin',
        ],
        'deluge.plugin.gtkui': [
            'TrackerStatus = deluge_trackerstatus:GtkUIPlugin',
        ],
        'deluge.plugin.web': [
            'TrackerStatus = deluge_trackerstatus:WebUIPlugin',
        ],
    },
)
