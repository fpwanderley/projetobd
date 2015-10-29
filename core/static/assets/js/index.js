cargaHoraria = "08:00:00";
updateTime = 0;
reversed = 1;
hours = 00;
minutes = 00;
seconds = 00;

function stringToTime(){
    hours = parseInt(cargaHoraria.substring(0,2));
    minutes = parseInt(cargaHoraria.substring(3,5));
    seconds = parseInt(cargaHoraria.substring(6));
}

$(document).ready(function() {
    $("#check_today").html(currentDay());
    $("#time_check").html(cargaHoraria);
    updateClock();
    stringToTime();
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

$(document).on({
    click: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            switch($(this).html()){
                case("Checkin"):
                    $(this).removeClass("btn-success");
                    $(this).addClass("btn-danger");
                    $(this).html("Checkout");
                    getStartTime();
                    updateTime = 1;
                break;
                case("Checkout"):
                    $(this).addClass("btn-success");
                    $(this).removeClass("btn-danger");
                    $(this).html("Checkin");
                    getEndTime();
                    resetTimer();
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

function resetTimer(){
    $("#time_check_hour").html("00");
    $("#time_check_minutes").html("00");
    $("#time_check_seconds").html("00");
}