odoo.define('acc_module.payment', function (require) {
    "use strict";

var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var rpc = require('web.rpc');
publicWidget.registry.payment = publicWidget.Widget.extend({
        selector: '.payment_container',
        events: {
            'click .addmore': 'add_payable_paymentline',
            'click .addmore_receivable': 'add_receivable_paymentline',
            'click .done_receivable' : 'make_receivable_payment',
            'click .done_payable' : 'make_payable_payment',
            'change .amount_receivable' : 'set_total_receivable',
            'change .amount_payable' : 'set_total_payable',
            'click .delete_line': 'delete_row',
            'input .amount_receivable' : 'validate_amount',
            'input .amount_payable' : 'validate_amount',
            'input .party_name' : 'complete_column',
            'input .case_type' : 'complete_column',
            'input .court_id' : 'complete_column',
            'input .court_employee_code' : 'complete_column',
            'input .rec_method' : 'complete_column',
            'input .pay_method': 'complete_column',


        },

        start: function () {
//            var table = jQuery('#payment_table');
//            var previous_no = document.getElementById("previous_number").value;
//            if(previous_no)
//            {   table.find('#serial_no').val(previous_no);}
//            else{   table.find('#serial_no').val(1); }
        },

        make_payable_payment : function(events){
        var current_button = $(events.currentTarget);
        var current_row = $(events.currentTarget).closest('tr');

//        PayMethod
        var pay_method = current_row.find('.pay_method').val();
        var pay_method_id = current_row.find('.pay_method').attr('id');


        var mpy_number = current_row.find('.mpy_number').val();
        var amount = current_row.find('.amount_payable').val();
        var payment_date = current_row.find('.payment_date').val();
        var mrc_number = current_row.find('.mrc_number').val();
        var draw_date = current_row.find('.draw_date').val();
        var bank_ref = current_row.find('.bank_ref').val();

//        CaseType
        var case_number = document.getElementsByClassName('case_number')[0].value;
        var case_number_id = jQuery('.case_number').attr('id');

//        PartyNumber
        var partner_number = current_row.find('.partner_number').val();
        var number_id = current_row.find('.partner_number').attr('id');

//        PartyName
        var party_name = document.getElementsByClassName('party_name')[0].value;
        var party_id = jQuery('.party_name').attr('id');

//        CourtEmployeeCode
        var employee_code = current_row.find('.court_employee_code').val();
        var employee_code_id = current_row.find('.court_employee_code').attr('id');

        var notes = document.getElementById('notes').value;

        var dict = { 'mrc_number': mrc_number, 'case_number': case_number, 'case_number_id': case_number_id,
                    'amount': amount, 'partner_id': party_name, 'party_id': party_id, 'bank_ref': bank_ref,
                    'notes': notes, 'pay_method': pay_method, 'pay_method_id': pay_method_id,
                    'payment_date': payment_date, 'mpy_number': mpy_number, 'partner_number': partner_number,
                    'number_id': number_id, 'court_emp_code': employee_code, 'employee_code_id': employee_code_id,
                    }
        if((mpy_number !== '') && (party_name !== '') && (case_number !== '') && (payment_date !== ''))
        {
                rpc.query({ model: 'account.payment',
                    method: 'make_payables',
                    args: ['', dict],
                })
                .then(function (data) {
                    $("#payment_message")[0].innerHTML = data['message'];
                    $("#payment_message")[0].style.display = '';
                    $("#payment_message").show().delay(1800).fadeOut()
                    if(data['check'] == 1)
                    {
                    current_row.find('td').each(function() {
                    $(this).find('input,select,textarea').attr("readonly", true);
                    });
                    current_button.attr("disabled", true);
                    }
                });
           }
        },

        make_receivable_payment : function(events){

        var current_button = $(events.currentTarget);
        var current_row = $(events.currentTarget).closest('tr');
        var case_number = current_row.find('.case_number').val();
        var mrc_number = current_row.find('.mrc_number').val();
        var amount = current_row.find('.amount_receivable').val();

//        CaseType
        var case_type = current_row.find('.case_type').val();
        var case_id = current_row.find('.case_type').attr('id');

//        PartyNumber
        var partner_number = current_row.find('.partner_number').val();
        var number_id = current_row.find('.partner_number').attr('id');

//        PartyName
        var party_name = current_row.find('.party_name').val();
        var party_id = current_row.find('.party_name').attr('id');

        var bank_dps = current_row.find('.bank_dps').val();
        var notes = current_row.find('.notes').val();
        var payment_date = document.getElementById('payment_date').value;

//        RecMethod
        var rec_method = document.getElementsByClassName('rec_method')[0].value;
        var rec_method_id = jQuery('.rec_method').attr('id');

//        Court
        var court = document.getElementsByClassName('court_id')[0].value;
        var court_id = jQuery('.court_id').attr('id');

//        courtEmployeeCode
        var employee_code = document.getElementsByClassName('court_employee_code')[0].value;
        var employee_code_id = jQuery('.court_employee_code').attr('id');

        var dict = {'case_number': case_number, 'mrc_number': mrc_number, 'amount': amount, 'case_type': case_type,
                    'partner_id': party_name, 'bank_dps': bank_dps, 'notes': notes, 'rec_method': rec_method,
                    'payment_date': payment_date, 'court': court, 'court_id': court_id, 'party_id': party_id,
                    'number_id': number_id, 'case_id': case_id, 'partner_number':partner_number,
                    'rec_method': rec_method, 'rec_method_id': rec_method_id, 'court_emp_code': employee_code,
                    'employee_code_id': employee_code_id,
        }

        if((mrc_number !== '') && (court !== '') && (employee_code !== '') && (rec_method !== '') && (payment_date !== ''))
        {
                    rpc.query({ model: 'account.payment',
                    method: 'make_receivables',
                    args: ['', dict],
                })
                .then(function (data) {
                    $("#payment_message")[0].innerHTML = data['message'];
                    $("#payment_message")[0].style.display = '';
                    $("#payment_message").show().delay(1800).fadeOut()
                    if(data['check'] == 1)
                    {
                    current_row.find('td').each(function() {
                    $(this).find('input,select,textarea').attr("readonly", true);
                    });
                    current_button.attr("disabled", true);
                    }

                });
        }

        },


        add_receivable_paymentline : function(events){
             var content = jQuery('#receivable_table tr:last'),
             element = null,
             element = content.clone();
             element.appendTo("#receivable_table > tbody");
             var no = parseInt(element.find('.serial_no').val());
             no += 1;
             element.find('.serial_no').val(no);
             element.find('.case_number').val('');
             element.find('.mrc_number').val('');
             element.find('.amount_receivable').val('');
             element.find('.case_type').val('');
             element.find('.party_number').val('');
             element.find('.party_name').val('');
             element.find('.bank_dps').val('');
             element.find('.notes').val('');
        },
             add_payable_paymentline : function(events){
             var content = jQuery('#payable_table tr:last'),
             element = null,
             element = content.clone();
             element.appendTo("#payable_table > tbody");
             var no = parseInt(element.find('.serial_no').val())
             no += 1;
             element.find('.serial_no').val(no);
             element.find('.pay_method').val('');
             element.find('.mpy_number').val('');
             element.find('.amount_payable').val('');
             element.find('.date').val('');
             element.find('.mrc_number').val('');
             element.find('.draw_date').val('');
             element.find('.bank_ref').val('');
             element.find('.notes').val('');attribute
        },

        set_total_receivable : function(events){
           var sum = 0;
           $('.amount_receivable').each(function() {
               var x = $(this).val();
               sum += parseFloat(x || 0);
            });
           $('#total_receivable_amount').val(sum);
        },

        set_total_payable : function(events){
            var sum = 0;
           $('.amount_payable').each(function() {
               var x = $(this).val();
               sum += parseFloat(x || 0);
            });
           $('#total_payable_amount').val(sum);
        },

        delete_row : function(events){
            var tbody = $("table tbody");
            if (tbody.children().length > 1) {
                $(events.currentTarget).closest('tr').remove();
            }
        },

        validate_amount : function(events){
        $(events.currentTarget).val($(events.currentTarget).val().replace(/[^0-9\.]/g, ''));
        },

        complete_column : function(events){
        var class_name = $(events.currentTarget).closest('td').find("input").attr("name");
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