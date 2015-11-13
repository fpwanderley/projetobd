$(document).ready(function() {
    $('#myDatepicker').datepicker({
        format: 'dd/mm/yyyy',
        startDate: '-30d',
        endDate: '0'
    });

    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
          .x(function(d) { return d.label })    //Specify the data accessors.
          .y(function(d) { return d.value })
          .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
          .tooltips(false)        //Don't show tooltips
          .showValues(true)       //...instead, show the bar value right on top of each bar.
          .transitionDuration(350)
          ;

        d3.select('#nvd3_chart svg')
          .datum([exampleData()])
          .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
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

//Each bar represents a single discrete quantity.
function exampleData() {
    data = {
      key: "Dias da semana",
      values: [
        { 
          "color" : "#2CA044",
          "label" : "Domingo" ,
          "value" : 6
        } , 
        { 
          "color" : "#D62728",
          "label" : "Segunda" , 
          "value" : 4
        } , 
        { 
          "label" : "Terça" , 
          "value" : 8
        } , 
        { 
          "label" : "Quarta" , 
          "value" : 6
        } , 
        { 
          "label" : "Quinta" ,
          "value" : 5
        } , 
        { 
          "label" : "Sexta" , 
          "value" : 7
        } , 
        { 
          "label" : "Sabado" , 
          "value" : 6
        }
      ]
    };
 return data;    

}