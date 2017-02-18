function plot_data() {
    $.getJSON("/get_data", function(data) {
        var grid = {
            gridLineWidth: 2,
            gridLineColor: 'rgb(235,235,235)',
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
//        alert(temperature_plot.join('\n'));
        $.jqplot ('chart', [temperature_plot, humidity_plot], {
            axes: {
                xaxis: {
                    renderer:$.jqplot.DateAxisRenderer
                }
            },
            grid: grid
        });
    });
}

$(document).ready(function() {
    plot_data();
//    setInterval(plot_data, 3000);
});
