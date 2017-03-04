function plot_data() {
    $.getJSON("/get_data", function(data) {
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

        $.jqplot ('chart', [brightness_plot, temperature_plot, humidity_plot], {
            axes: {
                xaxis: {
                    renderer: $.jqplot.DateAxisRenderer,
                    tickOptions: {
                        angle: 45,
                    }
                },
                yaxis: {
                    min:  0,
                    max: 40,
                    tickInterval: 2,
                    label: 'Temperature [°C]',
                },
                y2axis: {
                    min: 30,
                    max: 80,
                    tickInterval: 5,
                    label: 'Humidity [%]',
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
    });
}

function zero_pad(value) {
    if (value < 10) {
        value = '0' + value;
    }
    return value;
}

function pretty_print_unix_timestamp(stamp) {
    date = new Date(stamp*1000);
    year = date.getFullYear();
    month = zero_pad(date.getMonth()+1);
    day = zero_pad(date.getDate());
    hours = zero_pad(date.getHours());
    minutes = zero_pad(date.getMinutes());
    return [year, month, day].join('-') + ' ' + [hours, minutes].join(':');
};

function timeslotChanged(event, ui) {
    start = pretty_print_unix_timestamp($("#timeslot_slider").slider("values", 0));
    end = pretty_print_unix_timestamp($("#timeslot_slider").slider("values", 1));
    $("#timeslot_text_start").text(start);
    $("#timeslot_text_end").text(end);
};

$(document).ready(function() {
    $.getJSON("/get_available_timeslot", function(data) {
        min_ts = data[0][0]
        max_ts = data[1][0]
        left_slider = max_ts-60*60*24*7
        $("#timeslot_slider").slider({
            range: true,
            min: min_ts,
            max: max_ts,
            values: [left_slider, max_ts],
            slide: timeslotChanged
        });
    });
    plot_data();
});
