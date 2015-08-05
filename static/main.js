$(function() {
    var limit = location.href.match(/points\=(\d+)/);
    if (limit != null) {
        limit = parseInt(limit[1]);
    }
    $.get("./list" + (limit ? '?points=' + limit : ''), '', onData, 'text');
    
    function onData(data) {
        data = data.split(' ');
        var maxTs = parseInt(data[0].replace(/\:.+/, ''));
        var points = []
        for (var i = data.length - 1; i >= 0; i--) {
            var pts = data[i].split(':');
            points.push({
                x: (pts[0] - maxTs) / 86400,
                y: -parseInt(pts[1])}
            );
        }
        data = {
            series: [points]
        };
        var opt = {
            axisX: {type: Chartist.AutoScaleAxis, onlyInteger: true},
            axisY: {type: Chartist.AutoScaleAxis}};
        new Chartist.Line('#my-chart', data, opt);
    }
});
