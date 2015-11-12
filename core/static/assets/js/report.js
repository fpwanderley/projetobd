$(document).ready(function() {
    $('#myDatepicker').datepicker();
});

var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).on({
    change: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            console.log($(this).val());
            reportPost("month", $(this).val());
        } 
        return false;     
    }
}, "#select_month");

$(document).on({
    change: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            console.log($(this).val());
            reportPost("year", $(this).val());
        } 
        return false;     
    }
}, "#select_year");

var gate = 0;
$(document).on({
    change: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            if(gate){
                console.log($(this).val());
                reportPost("date", $(this).val());
            }
            gate = (gate + 1 ) % 2;
        } 
        return false;     
    }
}, "#date_input");

function reportPost(type, information){
    $.ajax({
      type: "POST",
      url: "/home/",
      data: {'type':type, 'info': information},
      success: function (data) {
        location.reload();
      },
      error: function(data) {
      }
    });
}