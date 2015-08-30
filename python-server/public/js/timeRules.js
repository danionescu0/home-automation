
timeRules = {
    updateURL: '/time-rules',

    init: function() {
        this.self = this;
        $( document ).ready(function() {
            $('.datepick').each(function(){
                $(this).timepicker({timeFormat: 'HH:mm:ss'});
            });
        });
        $( ".action-update" ).click(function() {
            console.log($(this).closest('tr'));
            console.log(timeRules);
            timeRules.update($(this).closest('tr'));
        });
    },

    update: function(trElem) {
        //console.log(trElem.find("input[class='rule_name']").val());
        $.ajax({
            url: this.updateURL,
            data: {
                type: 'update',
                rule: trElem.find("input[name='rule_name']").val(),
                actuator: trElem.find("select[name='actuator'] option:selected").val(),
                active: trElem.find("select[name='active'] option:selected").val(),
                state: trElem.find("select[name='state'] option:selected").val(),
                time: trElem.find("input[name='time']").val()
            },
            method: 'POST'
        })
    }
};

$( document ).ready(function() {
    timeRules.init();
});