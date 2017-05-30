// The plot object
// Set in plot()
var chart;

// Timestamp of the first shown data point
// Set in updateSliderLabels()
var start;

// Timestamp of the last shown data point
// Set in updateSliderLabels()
var end;

var brightness_series = {
    color: 'rgba(127, 127, 127, 0.3)',
    showMarker: false,
    shadow: false,
    fill: true,
};

var room_temperature_series = {
    yaxis: 'yaxis',
    color: 'rgba(255, 0, 0, 0.6)',
    showMarker: false,
    rendererOptions: {
        smooth: true
    },
};

var humidity_series = {
    yaxis: 'y2axis',
    color: 'rgba(0, 0, 255, 0.6)',
    showMarker: false,
    rendererOptions: {
        smooth: true
    },
};

var dew_point_series = {
    yaxis: 'yaxis',
    color: 'rgba(127, 127, 0, 0.6)',
    showMarker: false,
    rendererOptions: {
        smooth: true
    },
};

var chart_config = {
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
            min: 05,
            max: 35,
            tickInterval: 3,
            label: 'Temperature [°C]',
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
        },
        y2axis: {
            min: 25,
            max: 75,
            tickInterval: 5,
            label: 'Humidity [%]',
            labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
        }
    },

    series: [ brightness_series, room_temperature_series, humidity_series, dew_point_series ]
};

function plot(data) {
    brightness_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        brightness_plot.push([new Date(data.timestamp[i]), data.brightness[i]]);
    }
    humidity_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        humidity_plot.push([new Date(data.timestamp[i]), data.humidity[i]]);
    }
    room_temperature_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        room_temperature_plot.push([new Date(data.timestamp[i]), data.room_temperature[i]]);
    }
    dew_point_plot = []
    for (var i=0; i<data.timestamp.length; ++i) {
        dew_point = compute_dew(data.humidity[i], data.room_temperature[i]);
        dew_point_plot.push([new Date(data.timestamp[i]), dew_point]);
    }
    chart = $.jqplot('chart', [brightness_plot,
                               room_temperature_plot,
                               humidity_plot,
                               dew_point_plot],
                     chart_config);
    room_temperature_series = chart.series[1];
    humidity_series = chart.series[2];
    dew_point_series = chart.series[3];
}


function replot(event, ui) {
    $.getJSON('/get_data?start=' + start + '&end=' + end, function(data) {
        chart.destroy();
        plot(data);
    });
};

function updateSliderLabels(event, ui) {
    var prettyPrintTimestamp = function(stamp) {
        var zeroPad = function(value) {
            if (value < 10) {
                value = '0' + value;
            }
            return value;
        }
        var date = new Date(stamp*1000);
        var year = date.getFullYear();
        var month = zeroPad(date.getMonth()+1);
        var day = zeroPad(date.getDate());
        var hours = zeroPad(date.getHours());
        var minutes = zeroPad(date.getMinutes());
        return [year, month, day].join('-') + ' ' + [hours, minutes].join(':');
    };
    start = $('#timeslot_slider').slider('values', 0);
    end = $('#timeslot_slider').slider('values', 1);
    $('#timeslot_text_start').text(prettyPrintTimestamp(start));
    $('#timeslot_text_end').text(prettyPrintTimestamp(end));
};

$(document).ready(function() {
    $(window).resize(function() {
        chart.replot( { resetAxes: false } );
    });

    $.getJSON("/get_available_timeslot", function(data) {
        // Initialize time selection slider
        left_slider = data.end-60*60*24*7
        $("#timeslot_slider").slider({
            range:  true,
            min:    data.start,
            max:    data.end,
            values: [left_slider, data.end],
            slide:  updateSliderLabels,
            stop:   replot
        });
        updateSliderLabels();

        // Initial plot
        $.getJSON('/get_data?start=' + left_slider + '&end=' + data.end, function(data) {
            plot(data);
        });
    });
});
