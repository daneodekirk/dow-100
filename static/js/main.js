var points = [];
var globalopts = {
    sample : 1000 - 60 
};

jQuery(document).ready(function($) {

    $('#grapherror #close').click(function() {
        $('#grapherror').hide();
        return false;
    })

    $.ajaxSetup({
      "error":function() {   
        $('#grapherror').show().find('span')
            .html('There was a server error! Bugs happen. Try a different number.') 
    }});

    
});

function rendertime(js, py) {

    $('#rendertime').html( js + ' seconds');
    if(py !== undefined) 
        $('#pyrendertime').show().find('#pytime')
            .html( py.toFixed(5) + ' seconds');
    else 
        $('#pyrendertime').hide();
}
