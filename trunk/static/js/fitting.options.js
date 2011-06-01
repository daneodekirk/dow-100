var points = [];
$(document).ready(function() {

      var placeholder = $('#placeholder');
      var options = {
        series: {
           lines : {show : false},
           points: { show: true, fill: true}//, fillColor: "rgba(255, 255, 255, 0.8)" },
        },
        xaxis: { mode: "time", tickLength: 5 },
        zoom: { interactive: true }, 
        pan: { interactive: true },
      };

     $('#options input').each(function() {

       $(this).change(function() {
            var cache = points[0];
            points.length = 0;
            points.push(cache);

            var graphs = $(this).closest('ul').find(':checked');
            
            if(graphs.length > 0) {
                graphs.each(function() {
                    if(!this.checked) 
                        return;

                    var this_ = this;
                    var date = Date.now();

                    $.getJSON('/json', {
                        graph :this_.id, 
                        sample: globalopts.sample 
                    }, function(data) {
                            var d = {
                                'data'  : data.points, 
                                'color' : $(this_).attr('color'),
                                lines   : {show : true},
                                points  : { show: false}
                            };
                       
                           points.push(d);

                           $.plot(placeholder, points ,options);
                           //$('#rendertime').html((Date.now()-date)/1000 + 'seconds')
                           rendertime((Date.now()-date)/1000, data.time); 
                    });
                });
           } else {
               var date = Date.now();
               $.plot(placeholder, points ,options);
               //$('#rendertime').html((Date.now()-date)/1000 + 'seconds')
               rendertime((Date.now()-date)/1000);
           }

           $('#fittingoverview')
                .find('div').hide()
                .end()
                .find('.'+this.id).toggle(this.checked);

       })
     });

/*
     $.getJSON('/json', {graph: 'basic'}, function(data) {
        var d = {'data':data.points,'color':''};
        points.push(d);
        var plot = $.plot(placeholder, points, options);
        placeholder.data('graph', plot);
     });

     */

});
