main = {
    updateURL: '/',

    init: function() {
        $(":checkbox").bootstrapSwitch();
        $(":checkbox").on('switchChange.bootstrapSwitch', function (event, state) {
            main.update($(this).attr("name"), $(this).is(":checked"));
        });
        $(":button").click(function (event) {
            main.update($(this).attr("rel"), true);
        })
    },

    update: function(name, value) {
        $.ajax({
            url: this.updateURL,
            data: {
                actuator_name: name,
                actuator_value: value
            },
            method: 'POST'
        })
    },
};

$( document ).ready(function() {
    main.init();
});