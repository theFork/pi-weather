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

$(document).ready(function() {
    plot_data();
//    setInterval(plot_data, 3000);
});
