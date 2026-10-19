/**
 * TrackerStatus Plugin JavaScript for Deluge WebUI
 * Adds a "Tracker Status" column to the torrent grid.
 */
(function() {
    var KEY = 'tracker_status';
    var TITLE = 'Tracker Status';

    var TrackerStatusPlugin = Ext.extend(Deluge.Plugin, {
        name: 'TrackerStatus',

        constructor: function(config) {
            config = Ext.apply({
                name: 'TrackerStatus'
            }, config);
            TrackerStatusPlugin.superclass.constructor.call(this, config);
        },

        onEnable: function() {
            this.addGridColumn();
            if (window.deluge && deluge.events) {
                deluge.events.on('connect', this.addGridColumn, this);
            }
        },

        onDisable: function() {
            if (window.deluge && deluge.events) {
                deluge.events.un('connect', this.addGridColumn, this);
            }
            this.removeGridColumn();
        },

        addGridColumn: function() {
            var header = (typeof _ === 'function') ? _(TITLE) : TITLE;

            // 1. Ensure key is requested from daemon in Grid queries
            if (window.Deluge && Deluge.Keys && Deluge.Keys.Grid) {
                if (Deluge.Keys.Grid.indexOf(KEY) === -1) {
                    Deluge.Keys.Grid.push(KEY);
                }
            }

            // 2. Add column and field to TorrentGrid
            if (window.deluge && deluge.torrents) {
                var grid = deluge.torrents;

                // Ensure data field exists in store meta
                if (grid.meta && grid.meta.fields) {
                    var fieldFound = false;
                    Ext.each(grid.meta.fields, function(field) {
                        if (field.name === KEY) {
                            fieldFound = true;
                        }
                    });

                    if (!fieldFound) {
                        grid.meta.fields.push({ name: KEY });
                        if (grid.getStore() && grid.getStore().reader) {
                            grid.getStore().reader.onMetaChange(grid.meta);
                        }
                    }
                }

                // Ensure column exists in column model
                var colFound = false;
                Ext.each(grid.columns, function(col) {
                    if (col.dataIndex === KEY || col.id === KEY) {
                        colFound = true;
                    }
                });

                if (!colFound) {
                    var newCol = {
                        id: KEY,
                        header: header,
                        width: 160,
                        sortable: true,
                        renderer: function(value) {
                            if (!value) return '';
                            return Ext.util.Format.htmlEncode(value);
                        },
                        dataIndex: KEY
                    };

                    var newColumns = grid.columns.slice(0);
                    newColumns.push(newCol);
                    grid.colModel.setConfig(newColumns);
                    grid.columns = newColumns;
                }

                if (grid.getView()) {
                    grid.getView().refresh(true);
                }

                if (deluge.ui && deluge.ui.update) {
                    deluge.ui.update();
                }
            }
        },

        removeGridColumn: function() {
            if (window.deluge && deluge.torrents) {
                var grid = deluge.torrents;

                // Remove from store meta fields
                if (grid.meta && grid.meta.fields) {
                    var remainingFields = [];
                    Ext.each(grid.meta.fields, function(field) {
                        if (field.name !== KEY) {
                            remainingFields.push(field);
                        }
                    });
                    grid.meta.fields = remainingFields;
                    if (grid.getStore() && grid.getStore().reader) {
                        grid.getStore().reader.onMetaChange(grid.meta);
                    }
                }

                // Remove from columns
                var remainingCols = [];
                Ext.each(grid.columns, function(col) {
                    if (col.dataIndex !== KEY && col.id !== KEY) {
                        remainingCols.push(col);
                    }
                });
                grid.colModel.setConfig(remainingCols);
                grid.columns = remainingCols;

                if (grid.getView()) {
                    grid.getView().refresh(true);
                }
            }

            // Remove from Deluge.Keys.Grid
            if (window.Deluge && Deluge.Keys && Deluge.Keys.Grid) {
                var remainingKeys = [];
                Ext.each(Deluge.Keys.Grid, function(k) {
                    if (k !== KEY) {
                        remainingKeys.push(k);
                    }
                });
                Deluge.Keys.Grid = remainingKeys;
            }
        }
    });

    Deluge.registerPlugin('TrackerStatus', TrackerStatusPlugin);
})();
