/**
 * TorrentFilter Plugin JavaScript for Deluge WebUI
 * Adds a live name-filtering search input box to the Deluge toolbar.
 */
(function() {
    var TorrentFilterPlugin = Ext.extend(Deluge.Plugin, {
        name: 'TorrentFilter',
        currentQuery: '',

        constructor: function(config) {
            config = Ext.apply({
                name: 'TorrentFilter'
            }, config);
            TorrentFilterPlugin.superclass.constructor.call(this, config);
        },

        onEnable: function() {
            var self = this;
            this.addToolbarControls();
            this.hookTorrentGridUpdate();

            if (window.deluge && deluge.events) {
                deluge.events.on('connect', this.onConnect, this);
            }
        },

        onDisable: function() {
            if (window.deluge && deluge.events) {
                deluge.events.un('connect', this.onConnect, this);
            }
            this.unhookTorrentGridUpdate();
            this.clearFilter();
            this.removeToolbarControls();
        },

        onConnect: function() {
            this.addToolbarControls();
            this.hookTorrentGridUpdate();
        },

        addToolbarControls: function() {
            var self = this;
            if (!window.deluge || !deluge.toolbar) return;

            // If already added, don't duplicate
            if (Ext.getCmp('torrentFilterInput')) return;

            var toolbar = deluge.toolbar;

            // Find insertion point before Ext.Toolbar.Fill ('->')
            var insertIndex = -1;
            toolbar.items.each(function(item, idx) {
                if (item instanceof Ext.Toolbar.Fill || (item.id && item.id.indexOf('fill') !== -1)) {
                    insertIndex = idx;
                    return false;
                }
            });

            var sep = new Ext.Toolbar.Separator({ id: 'torrentFilterSep' });
            var label = new Ext.Toolbar.TextItem({
                id: 'torrentFilterLabel',
                text: ' <b style="color:#555;">' + _('Filter') + ':</b> '
            });

            var inputField = new Ext.form.TextField({
                id: 'torrentFilterInput',
                emptyText: _('Filter by name...'),
                width: 190,
                enableKeyEvents: true,
                listeners: {
                    keyup: function(field, e) {
                        if (e.getKey() === 27) { // Escape key
                            field.setValue('');
                            self.applyFilter('');
                            return;
                        }
                        self.applyFilter(field.getValue());
                    },
                    specialkey: function(field, e) {
                        if (e.getKey() === e.ENTER) {
                            e.stopEvent();
                        }
                    }
                }
            });

            var clearBtn = new Ext.Button({
                id: 'torrentFilterClearBtn',
                text: '✕',
                tooltip: _('Clear filter (Esc)'),
                handler: function() {
                    var field = Ext.getCmp('torrentFilterInput');
                    if (field) {
                        field.setValue('');
                    }
                    self.applyFilter('');
                }
            });

            var countBadge = new Ext.Toolbar.TextItem({
                id: 'torrentFilterCount',
                text: ''
            });

            var newItems = [sep, label, inputField, clearBtn, countBadge];

            if (insertIndex !== -1) {
                for (var i = 0; i < newItems.length; i++) {
                    toolbar.insert(insertIndex + i, newItems[i]);
                }
            } else {
                for (var j = 0; j < newItems.length; j++) {
                    toolbar.add(newItems[j]);
                }
            }

            toolbar.doLayout();
        },

        removeToolbarControls: function() {
            if (!window.deluge || !deluge.toolbar) return;
            var toolbar = deluge.toolbar;

            var controlIds = [
                'torrentFilterSep',
                'torrentFilterLabel',
                'torrentFilterInput',
                'torrentFilterClearBtn',
                'torrentFilterCount'
            ];

            Ext.each(controlIds, function(id) {
                var cmp = Ext.getCmp(id);
                if (cmp) {
                    toolbar.remove(cmp, true);
                }
            });

            toolbar.doLayout();
        },

        hookTorrentGridUpdate: function() {
            var self = this;
            if (!window.deluge || !deluge.torrents) return;
            if (deluge.torrents._origUpdate) return;

            deluge.torrents._origUpdate = deluge.torrents.update;
            deluge.torrents.update = function(torrents, wipe) {
                deluge.torrents._origUpdate.apply(this, arguments);

                if (self.currentQuery) {
                    self.applyFilter(self.currentQuery);
                } else {
                    self.updateCount();
                }
            };
        },

        unhookTorrentGridUpdate: function() {
            if (window.deluge && deluge.torrents && deluge.torrents._origUpdate) {
                deluge.torrents.update = deluge.torrents._origUpdate;
                delete deluge.torrents._origUpdate;
            }
        },

        applyFilter: function(query) {
            if (!window.deluge || !deluge.torrents) return;
            var store = deluge.torrents.getStore();
            if (!store) return;

            this.currentQuery = query ? query.trim() : '';

            if (!this.currentQuery) {
                store.clearFilter();
                this.updateCount();
                return;
            }

            var terms = this.currentQuery.toLowerCase().split(/\s+/);

            // Clear previous filter first so snapshot is based on complete dataset
            store.clearFilter(true);

            store.filterBy(function(record) {
                var name = record.get('name');
                if (!name) return false;
                var lowerName = name.toLowerCase();

                // Match all search terms
                for (var i = 0; i < terms.length; i++) {
                    if (lowerName.indexOf(terms[i]) === -1) {
                        return false;
                    }
                }
                return true;
            });

            this.updateCount();
        },

        clearFilter: function() {
            this.currentQuery = '';
            var input = Ext.getCmp('torrentFilterInput');
            if (input) {
                input.setValue('');
            }
            if (window.deluge && deluge.torrents) {
                var store = deluge.torrents.getStore();
                if (store) {
                    store.clearFilter();
                }
            }
            this.updateCount();
        },

        updateCount: function() {
            var countCmp = Ext.getCmp('torrentFilterCount');
            if (!countCmp) return;

            if (!window.deluge || !deluge.torrents) return;
            var store = deluge.torrents.getStore();
            if (!store) return;

            if (this.currentQuery) {
                var filtered = store.getCount();
                var total = store.snapshot ? store.snapshot.getCount() : filtered;
                var text = ' <span style="font-size:11px; color:#555; font-weight:bold;">(' + filtered + '/' + total + ')</span>';
                if (countCmp.setText) {
                    countCmp.setText(text);
                } else if (countCmp.getEl()) {
                    countCmp.getEl().update(text);
                }
            } else {
                if (countCmp.setText) {
                    countCmp.setText('');
                } else if (countCmp.getEl()) {
                    countCmp.getEl().update('');
                }
            }
        }
    });

    Deluge.registerPlugin('TorrentFilter', TorrentFilterPlugin);
})();
