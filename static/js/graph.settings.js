$(document).ready(function() {

    var placeholder = $('#placeholder');
    var graphopts = {
        series: {
            lines : {show : false},
            points: { show: true, fill: true}
        },
        xaxis: { mode: "time", tickLength: 5 },
        //grid: { hoverable: true},
        zoom: { interactive: true }, 
        pan: { interactive: true },
    };

    slideropts= {
        range: "min",
        value:60,
        min: 0,
        max: 999,
        step: 1,
        slide: function( event, ui ) {
            $( "#slidervalue" ).html( ui.value );
            globalopts.sample = (1000 - ui.value);
        },
        stop: function(event, ui) {
            $('#close').trigger('click');

            $('#options input').each(function() { 
                this.checked = false;
            });

            var graph = placeholder.data('graph');
              var options = {
                series: {
                   lines : {show : false},
                   points: { show: true, fill: true}
                },
                xaxis: { mode: "time", tickLength: 5 },
                zoom: { interactive: true }, 
                pan: { interactive: true },
              };

              _json(ui.value);

        }
    };

    $( "#slider" ).slider( slideropts );
    $('#slidervalue').html( slideropts.value );

    $('#chebyshevinput').live('keydown', function(e) {
        if(e.keyCode == 13) 
            _json(globalopts.sample);
    });

    _json(slideropts.value)

    function _json(sample) {
        var date = Date.now();
        $.getJSON('/json', {graph: 'basic', sample: (1000 - sample) }, function(data) {
           points.length = 0;

           var d = {'data':data.points,'color':''};
           points.push(d);

           $.plot(placeholder, points, graphopts);

           $('#sliderpoints').html( data.points.length );
           rendertime( (Date.now() - date)/1000, data.time );
           //$('#rendertime').html(  (Date.now() - date)/1000 + ' seconds' );

        });
    }

    /*
    $('#placeholder').bind("plothover", function (event, pos, item) {
//        if ($("#enableTooltip:checked").length > 0) {
            if (item) {
                if (previousPoint != item.dataIndex) {
                    previousPoint = item.dataIndex;
                    
                    var x = item.datapoint[0].toFixed(2),
                        y = item.datapoint[1].toFixed(2);
                    
                    $('#tooltip').css({
                        'top':item.pageX,
                        'left': item.pageY
                    }).html("( " + x + ", " + y + ")")
                        .fadeIn(200);
                }
            }
            else {
                $("#tooltip").hide();
                previousPoint = null;            
            }
//        }
    });
    
    */
    

});
