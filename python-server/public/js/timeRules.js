
timeRules = {
    actionsURL: '/time-rules',

    init: function() {
        $( document ).ready(function() {
            $('.datepick').each(function(){
                $(this).timepicker({timeFormat: 'HH:mm:ss'});
            });
        });
        $( ".action-update" ).click(function() {
            timeRules.update($(this).closest('tr'));
        });
        $( ".action-delete" ).click(function() {
            timeRules.delete($(this).closest('tr'));
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
                actuator: trElem.find("select[name='actuator'] option:selected").val(),
                active: trElem.find("select[name='active'] option:selected").val(),
                state: trElem.find("select[name='state'] option:selected").val(),
                time: trElem.find("input[name='time']").val()
            },
            method: 'POST',
            complete: function() {
                console.log('complete');
                var tr = trElem.find("input[name='rule_name']").parent().parent();
                console.log(tr);
                tr.css({backgroundColor: '#E3AF7B'});
                tr.animate({backgroundColor:'white'}, 1200);
            }
        })
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
    timeRules.init();
});