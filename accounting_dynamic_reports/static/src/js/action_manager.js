odoo.define('accounting_dynamic_reports.action_manager', function (require) {
"use strict";

    /**
     * The purpose of this file is to add the actions of type
     * 'ir_actions_xlsx_download' to the ActionManager.
     */

    var ActionManager = require('web.ActionManager');
    var CrashManager = require('web.CrashManager');
    var framework = require('web.framework');
    var session = require('web.session');

    ActionManager.include({

        /**
         * Executes actions of type 'ir_actions_xlsx_download'.
         *
         * @private
         * @param {Object} action the description of the action to execute
         * @returns {Deferred} resolved when the report has been downloaded ;
         *   rejected if an error occurred during the report generation
         */
        _executexlsxReportDownloadAction: function (action) {
            var self = this;
            framework.blockUI();
            return new Promise(function (resolve, reject) {
                session.get_file({
                    url: '/xlsx_reports',
                    data: action.data,
                    success: resolve,
                    error: (error) => {
                        self.call('crash_manager', 'rpc_error', error);
                        reject();
                    },
                    complete: framework.unblockUI,
                });
            });
        },
        /**
         * Overrides to handle the 'ir_actions_xlsx_download' actions.
         *
         * @override
         * @private
         */
        _handleAction: function (action, options) {
            if (action.type === 'ir_actions_xlsx_download') {
                return this._executexlsxReportDownloadAction(action, options);
            }
            return this._super.apply(this, arguments);
        },
    });

});
