from setuptools import find_packages, setup

__plugin_name__ = 'TorrentFilter'
__author__ = 'zapturk'
__author_email__ = 'zapturk@users.noreply.github.com'
__version__ = '0.1'
__url__ = 'https://github.com/deluge-torrent/deluge'
__license__ = 'GPLv3'
__description__ = 'Filter torrent names with an instant search input box'
__long_description__ = """Adds a search/filter input box to the Deluge interface to instantly filter torrents by name."""
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
            'TorrentFilter = deluge_torrentfilter:CorePlugin',
        ],
        'deluge.plugin.gtk3ui': [
            'TorrentFilter = deluge_torrentfilter:Gtk3UIPlugin',
        ],
        'deluge.plugin.gtkui': [
            'TorrentFilter = deluge_torrentfilter:GtkUIPlugin',
        ],
        'deluge.plugin.web': [
            'TorrentFilter = deluge_torrentfilter:WebUIPlugin',
        ],
    },
)
