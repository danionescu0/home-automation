ifttt = {
    actionsURL: '/ifttt',

    init: function() {
        $( ".action-update" ).click(function() {
            ifttt.update($(this).closest('tr'));
        });
        $( ".action-delete" ).click(function() {
            ifttt.delete($(this).closest('tr'));
        });
        $( ".new-rule" ).click(function() {
            $(".add-nwl-rule").show();
        });
    },

    update: function(trElem) {
        $.ajax({
            url: this.actionsURL,
            data: {
                type: 'update',
                rule: trElem.find("input[name='rule_name']").val(),
                data: trElem.find("textarea[name='rule_data']").val(),
                actuator: trElem.find("select[name='actuator'] option:selected").val(),
                active: trElem.find("select[name='active'] option:selected").val(),
                state: trElem.find("select[name='state'] option:selected").val(),
            },
            method: 'POST',
            complete: function(xhr) {
                if (xhr.status == 406) {
                    ifttt.showError(xhr.responseText);
                    return;
                }
                var tr = trElem.find("input[name='rule_name']").parent().parent();
                tr.css({backgroundColor: '#E3AF7B'});
                tr.animate({backgroundColor:'white'}, 1200);
            }
        })
    },

    showError: function (message) {
        $('#custom-alert').html(message);
        $('#custom-alert').show();
        $('#custom-alert').fadeOut(4000);
    },

    delete: function(trElem) {
        $.ajax({
            url: this.actionsURL,
            data: {
                type: 'delete',
                rule: trElem.find("input[name='rule_name']").val()
            },
            method: 'POST',
            complete: function() {
                trElem.find("input[name='rule_name']").parent().parent().remove();
            }
        })
    }
};

$( document ).ready(function() {
    ifttt.init();
});