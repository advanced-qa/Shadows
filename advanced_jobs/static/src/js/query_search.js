odoo.define('acc_module.query_search', function (require) {
    "use strict";

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
publicWidget.registry.query = publicWidget.Widget.extend({
        selector: '.query_container',
        events: {
            'change #search_by' : 'search_method',
            'click #button_search': 'submit_search',
            'click .edit_payment': 'edit_payment',
            'input .party_name' : 'complete_column',
            'input .case_type' : 'complete_column',
            'input .court_id' : 'complete_column',
            'input .court_employee_code' : 'complete_column',
            'input .rec_method' : 'complete_column',
            'input .pay_method': 'complete_column',
            'click .save_payment': 'save_payments',
        },

        search_method : function(events) {
        var search_id = $(events.currentTarget).val();
        if(search_id == 'date')
        {
            $('.from_date_td').show();
            $('.to_date_td').show();
            $('#search_input').hide();
        }else{
            $('#search_input').show();
            $('.from_date_td').hide();
            $('.to_date_td').hide();
        }
        },

        submit_search : function(events){
            $("form#search_payment").submit();
        },

        edit_payment : function(events){
            var row = $(events.currentTarget).data('key')
            var row_visible = $('#' + row).css('display');
            if(row_visible == 'none')
            {   $('#' + row).show();
            }else if(row_visible == 'table-row')
            {   $('#' + row).hide(); }
        },

        complete_column : function(events){
        var class_name = $(events.currentTarget).closest('td').attr("name");
        var current_row = $(events.currentTarget).closest('tr');
        $("."+ class_name).autocomplete({
        source: function(request, response) {
            $.ajax({
            url: "/search/fill",
            method: "POST",
            dataType: "json",
            data: { name: request.term, class_name: class_name},
            success: function( data ) {
                response( $.map( data, function( item ) {
                    return {
                        label: item.name,
                        value: item.name,
                        id: item.res_id,
                    }
                }));
            },
            error: function (error) {
               alert('error: ' + error);
            }
            });
        },
        select:function(suggestion,term,item){
        current_row.find('.'+ class_name).attr('id', term.item.id)
        },
        });
        },

        save_payments: function(events){
        var current_row = $(events.currentTarget).closest('tr');
        var record_id = current_row.attr('id');

        var partner_id = current_row.find('.party_name').val();
        var party_id = current_row.find('.party_name').attr('id');

        var rec_method = current_row.find('.rec_method').val();
        var rec_method_id = current_row.find('.rec_method').attr('id');

        var pay_method = current_row.find('.pay_method').val();
        var pay_method_id = current_row.find('.pay_method').attr('id');

        var court = current_row.find('.court_id').val();
        var court_id = current_row.find('.court_id').attr('id');

        var court_employee_code = current_row.find('.court_employee_code').val();
        var case_number = current_row.find('.case_number').val();

        var case_type = current_row.find('.case_type').val();
        var case_id = current_row.find('.case_type').attr('id');

        var mrc_number = current_row.find('.mrc_number').val();
        var mpy_number = current_row.find('.mpy_number').val();
        var bank_dps = current_row.find('.bank_dps').val();

        var dict = {'record_id': record_id, 'partner_id': partner_id, 'rec_method': rec_method, 'pay_method': pay_method,
                    'court': court, 'case_number': case_number, 'case_type': case_type, 'mrc_number': mrc_number,
                    'mpy_number': mpy_number, 'bank_dps': bank_dps, 'court_emp_code': court_employee_code,
                    'party_id': party_id, 'rec_method_id': rec_method_id, 'pay_method_id': pay_method_id,
                    'court_id': court_id, 'case_id': case_id}

        rpc.query({ model: 'account.payment',
                    method: 'edited_payment',
                    args: ['', dict],
                })
                .then(function (data) {
                    $('#' + record_id).hide();
                });
        },
        });
        });