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
                text: graphLeftText
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: graphRightText,
            data: datapointValues
        }]
    });
});