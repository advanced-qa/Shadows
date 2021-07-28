odoo.define('debrand.help_desk', function(require) {
  "use strict";
  var SystrayMenu = require('web.SystrayMenu');
  var core = require('web.core');
  var session = require('web.session');
  var Widget = require('web.Widget');
  var Qweb = core.qweb;

  var ActionMenu = Widget.extend({
    template: 'systray_cloud.myicon',
    events: {
      'click .my_icon': 'onclick_myicon',
    },
    onclick_myicon: function() {
        window.open("http://www.advanced.qa/helpdesk_support_ticket", '_blank');



    },
  });
  SystrayMenu.Items.push(ActionMenu);
  return ActionMenu;
});
