$(function () {
    $('#container').highcharts({
        title: {
            text: 'Home\'s graphs',
            x: -20 //center
        },
        xAxis: {
            categories: datapointDates
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '°C'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Tokyo',
            data: lightGraph
        }]
    });
});