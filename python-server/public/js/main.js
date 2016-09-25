main = {
    updateURL: '/',

    init: function() {
        $(":checkbox").bootstrapSwitch();
        $(":checkbox").on('switchChange.bootstrapSwitch', function (event, state) {
            main.update($(this));
        });
    },

    update: function(checkbox) {
        $.ajax({
            url: this.updateURL,
            data: {
                actuator_name: checkbox.attr("name"),
                actuator_value: checkbox.is(":checked")
            },
            method: 'POST',
        })
    },

};

$( document ).ready(function() {
    main.init();
});