odoo.define('acc_module.qnb_bank', function (require) {
    "use strict";

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
publicWidget.registry.qnb = publicWidget.Widget.extend({
        selector: '.qnb_container',
        events: {
            'input .case_type' : 'complete_column',
            'click .add_details' : 'add_bank_details',
            'click .addmore_lines': 'add_more_lines',
            'click .delete_line': 'delete_row',
        },


        add_more_lines : function(events){
             var content = jQuery('#qnb_table tr:last'),
             element = null,
             element = content.clone();
             element.appendTo("#qnb_table > tbody");
             var no = parseInt(element.find('.serial_no').val());
             no += 1;
             element.find('.serial_no').val(no);
             element.find('.case_number').val('');
             element.find('.case_type').val('');
             element.find('.payments_amount').val('');
             element.find('.receipts_amount').val('');
             element.find('.case_balance').val('');
        },

        delete_row : function(events){
           var tbody = $("table tbody");
           if (tbody.children().length > 1) {
                $(events.currentTarget).closest('tr').remove();
            }
        },

        add_bank_details : function(events){
        console.log("inside111")
        var current_button = $(events.currentTarget);
        var current_row = $(events.currentTarget).closest('tr');

        var case_number = current_row.find('.case_number').val();
        var case_type = current_row.find('.case_type').val();
        var case_type_id = current_row.find('.case_type').attr('id');
        var payments_amount = current_row.find('.payments_amount').val();
        var receipts_amount = current_row.find('.receipts_amount').val();
        var case_balance = current_row.find('.case_balance').val();


        var total_case_balance = $('#balance_case').val();
        var bank_balance = $('#bank_balance').val();
        var difference = $('#difference_bal').val();
        var date_of_statement = $('#date_of_statement').val();


        var dict = {'case_number': case_number, 'case_type': case_type, 'case_type_id': case_type_id,
        'payments_amount': payments_amount, 'receipts_amount': receipts_amount, 'case_balance': case_balance,
        'total_case_balance': total_case_balance, 'bank_balance': bank_balance, 'difference': difference,
        'date_of_statement': date_of_statement,
        }
                rpc.query({ model: 'qnb.account',
                method: 'make_record',
                args: ['', dict],
                })
                .then(function (data) {
                    $("#bank_message")[0].innerHTML = data['message'];
                    $("#bank_message")[0].style.display = '';
                    $("#bank_message").show().delay(1800).fadeOut()
                    if(data['check'] == 1)
                    {
                    current_row.find('td').each(function() {
                    $(this).find('input,select,textarea').attr("readonly", true);
                    });
                    current_button.attr("disabled", true);
                    }
                });


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

        });
});