$('div.maindialogContent').find('form').ready(function () {
    setTimeout(function () {

        var mainDialog = $('div.maindialogContent');
        var is_emplChecked = mainDialog.find('input#employee_email');
        var is_suplChecked = mainDialog.find('input#suplier_email');
        var is_selectData = $('select#selectData');
        var searchInput = $(' div.maindialogContent').find('input#searchBiodata');
        mainDialog.find(is_selectData).on('change', function () {
            if (is_selectData.val() != 'biodata') {
                searchInput.attr('disabled', 'true');
            } else if (is_selectData.val() == 'biodata') {
                searchInput.removeAttr('disabled')
                searchInput.click(function (event) {
                    event.preventDefault();
                    if (is_emplChecked.prop('checked') == false && is_suplChecked.prop('checked') == false) {
                        alert('Please select the Data to search Biodata')
                    } else {
                        searchInput.autocomplete({
                            source: function (request, response) {
                                $.ajax({
                                    url: url_searchBio(),
                                    method: 'POST',
                                    data: {
                                        'csrfmiddlewaretoken': get_csrf(),
                                        'is_empl': is_emplChecked.prop('checked'),
                                        'is_supl': is_suplChecked.prop('checked'),
                                        'term': searchInput.val()
                                    },
                                    success: function (data) {
                                        response(data);

                                    }
                                })

                            },
                            select: function (event, ui) {
                                mainDialog.find('div#searchBioContainer > div#resultSearch').append('<span id="resultBio" class="label label-success" data-value="' + ui.item.value + '">' + ui.item.label + '<i class="fa fa-close" style="margin-left: 7px;cursor: pointer;"></i></span>')
                                $('input#searchBiodata').val('')
                                $('div#searchBioContainer').find('i.fa-close').click(function () {
                                    $(this).parent().remove()
                                });
                                return false;
                            },
                        }).autocomplete("instance")._renderItem = function (ul, item) {
                            if (item.value.endsWith('-employee')) {
                                return $("<li>")
                                .append("<div>" + item.label + "<br><span style=\"font-size: 10px;color:#999999;vertical-align:text-bottom;clear:left\">nik : " + item.nik + "</span>" + "<span style=\"float:right;font-size:10px;clear:right;\">Employee</span>" + "</div>")
                                .appendTo(ul);
                            } else if (item.value.endsWith('-suplier')) {
                                return $("<li>")
                                .append("<div>" + item.label + "<br>" + item.value.match(/^\w+/) + "</div>")
                                .appendTo(ul);
                            }

                        };
                    }

                })



            }
        });
        //=================================== Convert to PDF =============================================
        var emailForm = NA.common.doc.querySelector('form#email_data');
        $('div.dialogButtonOKCancel>a.button:eq(0)').click(function (event) {
            var send_btn = NA.common.getElementID('emailData_submit');
            if (!emailForm.checkValidity()) {
                NA.NAEvent.preventDefault(event);
                send_btn.click();
            } else {
                if ($('span#successConvert').length == 0) {
                    alert('Please export to PDF before send email !!!')
                    //event.stopPropagation();
                } else {
                    function send_mailData() {
                        var data = {
                            'csrfmiddlewaretoken': get_csrf(),
                            'subject': $('input#id_subject').val(),
                            'message': $('textarea#id_message').val(),
                            'to': $('input#id_to').val()
                        };
                        var type_data = $('select#selectData').val();
                        if ($('select#selectData').val() == 'tabular_data') {
                            var data_report = []
                            if (is_emplChecked.prop('checked') == true) {
                                data_report.push('Employee')
                            };
                            if (is_suplChecked.prop('checked') == true) {
                                data_report.push('Suplier')
                            }
                            var send_mail = Object.assign({
                                'data_report_tabular': String(data_report),
                                'type_report': 'tabular_data'
                            }, data)
                        } else if ($('select#selectData').val() == 'biodata') {
                            var data_report_empl = []
                            var data_report_supl = []
                            $('span.label-success[data-value$=employee]').each(function () {
                                data_report_empl.push($(this).attr('data-value').replace('-employee', ''));
                            });
                            $('span.label-success[data-value$=suplier]').each(function () {
                                data_report_supl.push($(this).attr('data-value').replace('-suplier', ''));
                            });
                            var send_mail = Object.assign({
                                'type_report': 'biodata',
                                'data_report_empl': data_report_empl != '' ? String(data_report_empl) : 'none',
                                'data_report_supl': data_report_supl != '' ? String(data_report_supl) : 'none'
                            }, data)
                        }

                        return send_mail
                    }
                    $.ajax({
                        url: url_emailData(),
                        method: "POST",
                        data: send_mailData(),
                        beforeSend: function (data) {
                            $('div.containerDialog').remove()
                            $('div#dropSheet').append('<i style="position: absolute;z-index: 1000000;color: white;top: 4em;left: 9em;" class="fa fa-spinner fa-pulse fa-5x fa-fw"></i>')
                        },
                        success: function (data) {
                            $('div#dropSheet > i').removeClass('fa fa-spinner fa-pulse fa-5x fa-fw').addClass('fa fa-check fa-5x');
                            reload_LogEvent();
                        },
                        error: function (data) {
                            $('div#dropSheet > i').removeClass('fa fa-spinner fa-pulse fa-5x fa-fw').addClass('fa fa-window-close fa-5x')
                        },
                        complete: function (data) {
                            var dialog = NA.common.dialog.doc.querySelector("div.containerDialog");
                            setTimeout(function () {
                                NA.common.dialog.closeDialog(dialog);
                            }, 1000)

                        }
                    })
                }
            }
        });
        //================================= End Convert to PDF ===========================================

        $('div.bottomDialogContent').find('a.btn-link').click(function (event) {
            var target = NA.NAEvent.getTarget(event);
            var resultBio = mainDialog.find('span#resultBio');
            if (is_selectData.val() == 'tabular_data') {
                if (is_emplChecked.prop('checked') == false && is_suplChecked.prop('checked') == false) {
                    if (target.innerText.trim() == 'Preview PDF') {
                        alert('Please Select the Data to Preview PDF')
                    } else if (target.innerText.trim() == 'Export To PDF') {
                        alert('Please Select the Data to Export PDF')
                    }
                    return false
                } else {
                    if (is_emplChecked.prop('checked') == true) {
                        $.ajax({
                            url: url_emplData() + '?columnName=employee_name&valueKey=&dataType=Varchar&criteria=like&_search=false&nd=1517129972488&rows=100&page=1&sidx=idapp&sord=desc',
                            dataType: 'json',
                            beforeSend: function (jqXHR) {
                                var csrf_token = get_csrf();
                                jqXHR.setRequestHeader('X-CSRF_Token', csrf_token);
                            },
                            success: function (data) {
                                var doc = new jsPDF();
                                var get_data = data['rows']
                                var column = ['Nik', 'Employee Name', 'Type App', 'Job type', 'Gender', 'Status', 'Telp/Hp', 'Territory']
                                var rowsEmployee = []
                                for (var i = 0; i < get_data.length; i++) {
                                    rowsEmployee.push(get_data[i]['cell'].slice(1, 9)) //slice idapp
                                }
                                console.log(rowsEmployee)
                                doc.autoTable(column, rowsEmployee, {
                                    headerStyles: { fillColor: [231, 76, 60] }
                                });
                                if (target.innerText.trim() == 'Export To PDF') {//5432
                                    var val_empl = btoa(doc.output());
                                    $.ajax({
                                        url: url_emailUpl(),
                                        method: 'POST',
                                        beforeSend: function (jqXHR) {
                                            jqXHR.setRequestHeader('X-CSRF-Token', get_csrf())
                                        },
                                        data: {
                                            'csrfmiddlewaretoken': get_csrf(),
                                            'is_empl': is_emplChecked.prop('checked'),
                                            'is_supl': 'false',
                                            'toPDF_empl': val_empl
                                        },
                                        success: function (data) {
                                            if ($('span#successConvert').length == 0) {
                                                $('div.dialogButtonRightOther').append('<span id="successConvert" class="fa fa-check" style="color: #4CAF50;">Success</span>')
                                            }
                                        }
                                    })
                                } else if (target.innerText.trim() == 'Preview PDF') {
                                    doc.output('dataurlnewwindow')
                                }

                            }
                        })
                    };

                    if (is_suplChecked.prop('checked') == true) {
                        $.ajax({
                            url: url_suplData() + '?columnName=supliername&valueKey=&dataType=Varchar&criteria=like&_search=false&nd=1517132750079&rows=20&page=1&sidx=createddate&sord=desc',
                            dataType: 'json',
                            beforeSend: function (jqXHR) {
                                var csrf_token = get_csrf();
                                jqXHR.setRequestHeader('X-CSRF-Token', csrf_token);
                            },
                            success: function (data) {
                                var doc = new jsPDF();
                                var get_data = data['rows']
                                var column = ['Suplier Code', 'Suplier Name', 'Address', 'Telp', 'Hp', 'Contact Person']
                                var rowsSuplier = []
                                for (var i = 0; i < get_data.length; i++) {
                                    rowsSuplier.push(get_data[i]['cell'].slice(0, 6)) //slice inactive & createddate
                                }
                                //var rows = $.map(get_data, function (value, index) {
                                //    return [[value.supliercode, value.supliername, value.address, value.telp, value.hp, value.contactperson, value.inactive]];
                                //});
                                console.log(rowsSuplier)
                                doc.autoTable(column, rowsSuplier, {
                                    styles: {
                                        fontSize: 9,
                                    },
                                    margin: 5,
                                    columnStyles: {
                                        'Suplier Code': {
                                            lineWidth: 2
                                        }
                                    }
                                });
                                //doc.output('dataurlnewwindow')
                                if (target.innerText.trim() == 'Export To PDF') {
                                    var val_supl = btoa(doc.output());
                                    $.ajax({
                                        url: url_emailUpl(),
                                        beforeSend: function (jqXHR) {
                                            var csrf_token = get_csrf();
                                            jqXHR.setRequestHeader('X-CSRF-Token', csrf_token);
                                        },
                                        method: 'POST',
                                        data: {
                                            'csrfmiddlewaretoken': get_csrf(),
                                            'is_supl': is_suplChecked.prop('checked'),
                                            'is_empl': 'false',
                                            'toPDF_supl': val_supl
                                        },
                                        success: function (data) {
                                            if ($('span#successConvert').length == 0) {
                                                $('div.dialogButtonRightOther').append('<span id="successConvert" class="fa fa-check" style="color: #4CAF50;">Success</span>')
                                            }
                                        }

                                    });
                                } else if (target.innerText.trim() == 'Preview PDF') {
                                    doc.output('dataurlnewwindow')
                                }

                            }
                        });
                    };

                }
            } else if (is_selectData.val() == 'biodata') {
                if (is_emplChecked.prop('checked') == false && is_suplChecked.prop('checked') == false) {
                    alert('Please Search the data to Export PDF')
                    return false
                } else {
                    match_dataAutoComp = $('span.label-success');
                    match_bioEmpl = $('span.label-success[data-value$=employee]');
                    match_bioSupl = $('span.label-success[data-value$=suplier]');
                    function getBio_empl() {
                        if (match_bioEmpl.length > 0) {
                            var get_valueBio = []
                            if (match_bioEmpl.length > 1) {
                                match_bioEmpl.each(function () {
                                    get_valueBio.push($(this).attr('data-value').replace('-employee', ''));//show expression (for debug)
                                });
                                //for (var i = 0; i < match_dataAutoComp.length; i++) {
                                //    get_valueBio.push(match_dataAutoComp[i].attributes['value']['nodeValue'].replace('-employee', ''));
                                //}
                            } else if (match_bioEmpl.length == 1) {
                                get_valueBio.push(parseInt(match_bioEmpl.attr('data-value').match(/\d+/)))
                            } else {
                                return ""
                            }
                            return String(get_valueBio)
                        }
                    };
                    function getBio_supl() {
                        if (match_bioSupl.length > 0) {
                            var get_valueSupl = []
                            if (match_bioSupl.length > 1) {
                                match_bioSupl.each(function () {
                                    get_valueSupl.push($(this).attr('data-value').replace('-suplier', ''));
                                });
                            } else if (match_bioSupl.length == 1) {
                                get_valueSupl.push(match_bioSupl.attr('data-value').match(/^\w+/));
                            } else {
                                return ""
                            }
                            return String(get_valueSupl)
                        }
                    };

                    $.ajax({
                        url: url_retriveBio(),
                        method: "POST",
                        beforeSend: function (jqXHR) {
                            jqXHR.setRequestHeader('X-CSRF-Token', get_csrf())
                        },
                        data: {
                            "csrfmiddlewaretoken": get_csrf(),
                            "toPDF_type": is_selectData.val(),
                            //"is_empl": is_emplChecked.prop('checked'),
                            "total_bioEmpl": match_bioEmpl.length,
                            "bio_empl_idapp": getBio_empl(), //typeof match_dataAutoComp != 'undefined' && match_dataAutoComp.endsWith('employee') ? parseInt(match_dataAutoComp.match(/\d+/)) : ""
                            //"is_supl": is_suplChecked.prop('checked'),
                            "total_bioSupl": match_bioSupl.length,
                            "bio_supliercode": getBio_supl(),
                        },
                        success: function (data) {
                            var get_data_empl = data['employee']
                            var get_data_supl = data['suplier']
                            var empl_doc = new jsPDF();
                            if (get_data_empl) {
                                var column_empl = ['Nik', 'Employee Name', 'Type App', 'Job type', 'Gender', 'Status', 'Telp/Hp', 'Territory']
                                var rows_empl = $.map(get_data_empl, function (value, index) {
                                    return [[value.nik, value.employee_name, value.typeapp, value.jobtype, value.gender, value.status, value.telphp, value.territory]];
                                });
                                empl_doc.autoTable(column_empl, rows_empl, {
                                    headerStyles: { fillColor: [231, 76, 60] }
                                });
                            };
                            var supl_doc = new jsPDF();
                            if (get_data_supl) {
                                var column_supl = ['Suplier Code', 'Suplier Name', 'Address', 'Telp', 'Hp', 'Contact Person']
                                var rows_supl = $.map(get_data_supl, function (value, index) {
                                    return [[value.supliercode, value.supliername, value.address, value.telp, value.hp, value.contactperson]];
                                });
                                supl_doc.autoTable(column_supl, rows_supl, {
                                    styles: {
                                        fontSize: 9,
                                    },
                                    margin: 5,
                                    columnStyles: {
                                        'Suplier Code': {
                                            lineWidth: 2
                                        }
                                    }
                                });
                            }


                            if (target.innerText.trim() == 'Export To PDF') {
                                var val_bioEmpl = btoa(empl_doc.output());
                                var val_bioSupl = btoa(supl_doc.output());
                                $.ajax({
                                    url: url_emailUpl(),
                                    method: 'POST',
                                    beforeSend: function (jqXHR) {
                                        jqXHR.setRequestHeader('X-CSRF-Token', get_csrf())
                                    },
                                    data: {
                                        'csrfmiddlewaretoken': get_csrf(),
                                        'is_empl': match_bioEmpl.length > 0 ? 'true' : 'false',
                                        'is_supl': match_bioSupl.length > 0 ? 'true' : 'false',
                                        'toPDF_empl': val_bioEmpl ? val_bioEmpl : 'none',
                                        'toPDF_supl': val_bioSupl ? val_bioSupl : 'none'
                                    },
                                    success: function (data) {
                                        if ($('span#successConvert').length == 0) {
                                            $('div.dialogButtonRightOther').append('<span id="successConvert" class="fa fa-check" style="color: #4CAF50;">Success</span>')
                                        }
                                    }
                                })
                            } else if (target.innerText.trim() == 'Preview PDF') {
                                doc.output('dataurlnewwindow')
                            }

                        }
                    })
                }
            }


            //var toPDF_type = mainDialog.find('select#selectData');
            //if (toPDF_type.val() == 'tabular_data') {

            //    if (is_emplChecked.prop('checked') == false && is_suplChecked.prop('checked') == false) {
            //        alert('Please Select the Table for exporting PDF')
            //    }

            //} else if (toPDF_type.val() == 'biodata') {

            //}





        });
        //===================================== End Convert to PDF ============================================
    }, 1000)
});