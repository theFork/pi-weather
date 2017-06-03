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

    highlighter: {
        show: true,
        tooltipContentEditor: function(str, seriesIndex, pointIndex) {
            var timestamp = room_temperature_series.data[pointIndex][0];
            var room_temp = room_temperature_series.data[pointIndex][1].toFixed(1);
            var humidity = humidity_series.data[pointIndex][1];
            var dew_point = dew_point_series.data[pointIndex][1].toFixed(1);
            return '<table><tr>'
                 + `<td>Date:</td><td>${formatDate(timestamp)}</td>`
                 + '</tr><tr>'
                 + `<td>Time:</td><td>${formatTime(timestamp)}</td>`
                 + '</tr><tr>'
                 + `<td>Room temperature:</td><td>${room_temp}°C</td>`
                 + '</tr><tr>'
                 + `<td>Humidity:</td><td>${humidity}&emsp;%</td>`
                 + '</tr><tr>'
                 + `<td>Dew point:</td><td>${dew_point}°C</td>`
                 + '</tr></table>';
        },
    },

    series: [ brightness_series, room_temperature_series, humidity_series, dew_point_series ]
};

function formatDate(stamp) {
    var date = new Date(stamp);
    var year = date.getFullYear();
    var month = zeroPad(date.getMonth()+1);
    var day = zeroPad(date.getDate());
    return [year, month, day].join('-');
}

function formatTime(stamp) {
    var date = new Date(stamp);
    var hours = zeroPad(date.getHours());
    var minutes = zeroPad(date.getMinutes());
    return [hours, minutes].join(':');
}

function plot(evt) {
    var convert = function(data) {
        brightness_data = []
        for (var i=0; i<data.timestamp.length; ++i) {
            brightness_data.push([new Date(data.timestamp[i]), data.brightness[i]]);
        }
        humidity_data = []
        for (var i=0; i<data.timestamp.length; ++i) {
            humidity_data.push([new Date(data.timestamp[i]), data.humidity[i]]);
        }
        room_temperature_data = []
        for (var i=0; i<data.timestamp.length; ++i) {
            room_temperature_data.push([new Date(data.timestamp[i]), data.room_temperature[i]]);
        }
        dew_point_data = []
        for (var i=0; i<data.timestamp.length; ++i) {
            dew_point = compute_dew(data.humidity[i], data.room_temperature[i]);
            dew_point_data.push([new Date(data.timestamp[i]), dew_point]);
        }
        return [brightness_data, room_temperature_data, humidity_data, dew_point_data];
    };
    var doPlot = function(data) {
        if (chart) {
            chart.destroy();
        }
        chart = $.jqplot('chart', data, chart_config);
        room_temperature_series = chart.series[1];
        humidity_series = chart.series[2];
        dew_point_series = chart.series[3];
    };

    if (evt == 'resize') {
        doPlot(chart.data);
    }
    else {
        $.getJSON(`/get_data?start=${start}&end=${end}`, function(data) {
            doPlot(convert(data));
        });
    }
}

function zeroPad(value) {
    if (value < 10) {
        value = '0' + value;
    }
    return value;
}

$(document).ready(function(evt) {
    var eventHandler = function(evt) {
        plot(evt.type);
    };

    $(window).resize(eventHandler);

    $.getJSON("/get_available_timeslot", function(data) {
        // Initialize time selection slider
        $("#timeslot_slider").slider({
            range:  true,
            min:    data.start,
            max:    data.end,
            values: [data.end-60*60*24*7, data.end],
            stop:   eventHandler,
        });

        // Bind event handler and trigger initial slider label update
        $("#timeslot_slider").on('slide', function() {
            start  = $('#timeslot_slider').slider('values', 0);
            end  = $('#timeslot_slider').slider('values', 1);
            var formatTimestamp = function(timestamp) {
                return formatDate(timestamp) + ' ' + formatTime(timestamp);
            };
            $('#timeslot_text_start').text(formatTimestamp(start*1000));
            $('#timeslot_text_end').text(formatTimestamp(end*1000));
        });
        $("#timeslot_slider").trigger('slide');

        // Initial plot
        plot('load');
    });
});
