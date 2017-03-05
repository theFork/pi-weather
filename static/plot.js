function plot(data) {
    var grid = {
        gridLineColor: 'rgb(200,200,200)',
        drawGridlines: true
    };
    temperature_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        temperature_plot.push([new Date(data.timestamp[i]), data.temperature[i]]);
    }
    humidity_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        humidity_plot.push([new Date(data.timestamp[i]), data.humidity[i]]);
    }
    brightness_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        brightness_plot.push([new Date(data.timestamp[i]), data.brightness[i]]);
    }

    $('#chart').empty();
    $.jqplot ('chart', [brightness_plot, temperature_plot, humidity_plot], {
        axes: {
            xaxis: {
                renderer: $.jqplot.DateAxisRenderer,
                rendererOptions: {
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions: {
                        angle: -45,
                    },
                },
            },
            yaxis: {
                min: 10,
                max: 30,
                tickInterval: 2,
                label: 'Temperature [°C]',
                labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            },
            y2axis: {
                min: 30,
                max: 80,
                tickInterval: 5,
                label: 'Humidity [%]',
                labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
            }
        },
        grid: grid,
        series: [
            { // Luminosity
                color: 'rgba(127, 127, 127, 0.3)',
                showMarker: false,
                shadow: false,
                fill:true,

            },
            { // Temperature
                yaxis: 'yaxis',
                color: 'rgba(255, 0, 0, 0.6)',
                showMarker: false,
                rendererOptions: {
                    smooth: true
                },
            },
            { // Humidity
                yaxis: 'y2axis',
                color: 'rgba(0, 0, 255, 0.6)',
                showMarker: false,
                rendererOptions: {
                    smooth: true
                },
            },
        ]
    });
}

function zeroPad(value) {
    if (value < 10) {
        value = '0' + value;
    }
    return value;
}

function prettyPrintTimestamp(stamp) {
    date = new Date(stamp*1000);
    year = date.getFullYear();
    month = zeroPad(date.getMonth()+1);
    day = zeroPad(date.getDate());
    hours = zeroPad(date.getHours());
    minutes = zeroPad(date.getMinutes());
    return [year, month, day].join('-') + ' ' + [hours, minutes].join(':');
};

function updateSliderLabels(event, ui) {
    start = $('#timeslot_slider').slider('values', 0);
    end = $('#timeslot_slider').slider('values', 1);
    $('#timeslot_text_start').text(prettyPrintTimestamp(start));
    $('#timeslot_text_end').text(prettyPrintTimestamp(end));
};

function replot(event, ui) {
    $.getJSON('/get_data?start=' + start + '&end=' + end, function(data) {
        plot(data);
    });
};

$(document).ready(function() {
    $.getJSON("/get_available_timeslot", function(data) {
        // Initialize time selection slider
        min_ts = data[0]
        max_ts = data[1]
        left_slider = max_ts-60*60*24*7
        $("#timeslot_slider").slider({
            range:  true,
            min:    min_ts,
            max:    max_ts,
            values: [left_slider, max_ts],
            slide:  updateSliderLabels,
            stop:   replot
        });
        updateSliderLabels();

        // Initial plot
        $.getJSON('/get_data?start=' + left_slider + '&end=' + max_ts, function(data) {
            plot(data);
        });
    });
});
