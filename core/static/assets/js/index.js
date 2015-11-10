cargaHoraria = "08:00:00";
updateTime = 0;
reversed = 1;
hours = 00;
minutes = 00;
seconds = 00;
exit_hours = 00;
exit_minutes = 00;
exit_seconds = 00;
exit_time = "xx:xx:xx";

function stringToTime(){
    if(cargaHoraria.substring(0,1) == "-"){
        reversed = 0;
        $("#time_check").removeClass("text-danger");
        $("#time_check").addClass("text-success");
        cargaHoraria = cargaHoraria.substring(1);
    }
    hours = parseInt(cargaHoraria.substring(0,2));
    minutes = parseInt(cargaHoraria.substring(3,5));
    seconds = parseInt(cargaHoraria.substring(6));
    
}

function exitStringToTime(){
    exit_hours = parseInt(exit_time.substring(0,2));
    exit_minutes = parseInt(exit_time.substring(3,5));
    exit_seconds = parseInt(exit_time.substring(6));
}

$(document).ready(function() {
    if($("#check_today").html() == "xx/xx/xxxx"){
        $("#check_today").html(currentDay());
    }
    if($("#time_check").html() == "xx:xx:xx"){
        $("#time_check").html(cargaHoraria);
    }else{
        cargaHoraria = $("#time_check").html();
    }
    if($("#check_button").html() == "Checkout"){
        updateTime = 1;
    }
    exit_time = $("#exit_time").html();
    exitStringToTime();
    stringToTime();
    updateClock();
    updateExit();
})

function updateClock(){
    if( updateTime == 1 ){
        if( reversed ){
            seconds -= 1;
            if( seconds <= 0 ){
                seconds = 59;
                minutes -= 1;
                if( minutes <= 0 ){
                    minutes = 59;
                    hours -= 1;
                    if(hours < 0){
                        reversed = 0;
                        hours = 0;
                        minutes = 0;
                        seconds = 0;
                        $("#time_check").removeClass("text-danger");
                        $("#time_check").addClass("text-success");
                    }
                }
            }
        }else{
           seconds += 1;
            if( seconds >= 60 ){
                seconds = 0;
                minutes += 1;
                if( minutes >= 60 ){
                    minutes = 0;
                    hours += 1;
                }
            } 
        }
        $("#time_check").html(timeToString(hours,minutes,seconds));
    }
    setTimeout(updateClock, 1000);
}

function updateExit(){
    if( !updateTime ){
        if (reversed){
            exit_seconds += 1;
            if( exit_seconds >= 60 ){
                exit_seconds = 0;
                exit_minutes += 1;
                if( exit_minutes >= 60 ){
                    exit_minutes = 0;
                    exit_hours += 1;
                }
            }   
        }
        $("#exit_time").html(timeToString(exit_hours,exit_minutes,exit_seconds));
    }
    setTimeout(updateExit, 1000);
}

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

function checkPost(check){
    $.ajax({
      type: "POST",
      url: "/home/",
      data: {'check': check},
      success: function (data) {
        location.reload();
      },
      error: function(data) {
      }
    });
}


$(document).on({
    click: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            switch($(this).html()){
                case("Checkin"):
                    checkPost("Checkin");
                    $(this).removeClass("btn-success");
                    $(this).addClass("btn-danger");
                    $(this).html("Checkout");
                    $("#checkin_title").html("Checkout");
                    getStartTime();
                    updateTime = 1;
                break;
                case("Checkout"):
                    checkPost("Checkout");
                    $(this).addClass("btn-success");
                    $(this).removeClass("btn-danger");
                    $(this).html("Checkin");
                    $("#checkin_title").html("Checkin");
                    getEndTime();
                    updateTime = 0;
                break;
            }
        } 
        return false;     
    }
}, "#check_button");

function currentDay(){
    var currentTime = new Date();
    d = currentTime.getDate();
    var d_sep = d < 10 ? "0" : "";
    m = currentTime.getMonth()+1;
    var m_sep = m < 10 ? "/0" : "/";
    a = currentTime.getFullYear();
    return d_sep + d + m_sep + m + "/" + a;
}

function timeToString(h,m,s){
    var h_sep = h < 10 ? "0" : "";
    var m_sep = m < 10 ? ":0" : ":";
    var s_sep = s < 10 ? ":0" : ":";
    return h_sep + h + m_sep + m + s_sep + s;
}

function currentTimeToString(){
    var currentTime = new Date();
    var h = currentTime.getHours();
    var h_sep = h < 10 ? "0" : "";
    var m = currentTime.getMinutes();
    var m_sep = m < 10 ? ":0" : ":";
    var s = currentTime.getSeconds();
    var s_sep = s < 10 ? ":0" : ":";
    return h_sep + h + m_sep + m + s_sep + s;
}

function getStartTime(){
    $("#check_times").append("<p class='fs-14 margin_bottom_0px'>"+currentTimeToString()+" - </p>");
}

function getEndTime(){
    $("#check_times").children().last().html($("#check_times").children().last().html()+currentTimeToString());
}
