var options = {
    series: [],
    chart: {
        height: 1000,
        type: 'candlestick',
    },
    title: {
        text: 'CandleStick Chart - Category X-axis',
        align: 'left'
    },
    tooltip: {
        enabled: true,
    },
    xaxis: {
        type: 'category',
        labels: {
            formatter: function(val) {
                return dayjs.unix(val).format('HH:mm')
            }
        }
    },
    yaxis: {
        tooltip: {
            enabled: true
        }
    }
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

var url = '/chart';

$.getJSON(url, function(response) {
    // Generated data from server side
    data = response[0]

    // Generated annotation from server side
    annotation_dict = response[1]

    // Title
    title = response[2]

    // Update Data
    chart.updateSeries([{
        name: 'Candles',
        data: data
    }])

    // Update X axis Information, e.g. Candle Patterns etc.
    // The list of annotation needs to be iterated to add details
    for (let i = 0; i < annotation_dict.length; i++) {
        chart.addXaxisAnnotation(annotation_dict[i]);
    }

    chart.updateOptions({
      title: {
        text: title
      }
    })

});