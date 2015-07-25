$(function() {
    
    $.get("./list", '', onData, 'text');
    
    function onData(data) {
        data = '1437808443:463211 1437718440:453469 1437635640:451887 1437549242:450392 1437455641:450314 1437362041:448258 1437286442:440935 1437218040:435965 1437135244:457139 1437034444:455177 1437016387:451144';
        data = data.split(' ');
        var ts = [];
        var points = []
        for (var i = data.length - 1; i >= 0; i--) {
            var pts = data[i].split(' ');
            ts.push(parseInt(pts[0]));
            points.push(parseInt(pts[1]));
        }
        data = {
            labels: ts,
            series: [points]
        };
        new Chartist.Line('#my-chart', data);
    }
});
