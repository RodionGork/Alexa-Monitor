$(function() {
    
    $.get("./list", '', onData, 'text');
    
    function onData(data) {
        data = data.split(' ');
        var ts = [];
        var points = []
        for (var i = data.length - 1; i >= 0; i--) {
            var pts = data[i].split(':');
            ts.push('x-' + i);
            points.push(-parseInt(pts[1]));
        }
        data = {
            labels: ts,
            series: [points]
        };
        new Chartist.Line('#my-chart', data);
    }
});
