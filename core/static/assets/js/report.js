$(document).ready(function() {
    $('#myDatepicker').datepicker({
        format: 'dd/mm/yyyy',
        startDate: '-30d',
        endDate: '0'
    });
    generate_chart(myData);
});

function generate_chart(data){
    if(report_type == "user"){   
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
              .datum([data])
              .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }else if (report_type == "adm"){
        nv.addGraph(function() {
            var chart = nv.models.multiBarHorizontalChart()
                .x(function(d) { return d.label })
                .y(function(d) { return d.value })
                .margin({top: 30, right: 20, bottom: 50, left: 175})
                .showValues(true)           //Show bar value next to each bar.
                .tooltips(true)             //Show tooltips on hover.
                .transitionDuration(350)
                .showControls(true);        //Allow user to switch between "Grouped" and "Stacked" mode.

            chart.yAxis
                .tickFormat(d3.format(',.2f'));
            // Talvez tenha que por o data em uma lista
            d3.select('#nvd3_chart svg')
                .datum([data])
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });
    }
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

function deselectSelectBox(selector){
    $(selector+' option:selected').removeAttr('selected');
    $(selector).find('option[value="-"]').attr("selected",true);
}

$(document).on({
    change: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            reportPost("month", $(this).val());
            $("#date_input").val('');
            deselectSelectBox("#select_year");
        } 
        return false;     
    }
}, "#select_month");

$(document).on({
    change: function (event) {
        if (event.handled !== true) {
            event.handled = true;
            reportPost("year", $(this).val());
            $("#date_input").val('');
            deselectSelectBox("#select_month");
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
                reportPost("date", $(this).val());
                deselectSelectBox("#select_year");
                deselectSelectBox("#select_month");
            }
            gate = (gate + 1 ) % 2;
        } 
        return false;     
    }
}, "#date_input");

function reportPost(request_type, selected_date){
    $.ajax({
      type: "POST",
      url: "/report/",
      data: {'request_type':request_type, 'selected_date': selected_date},
      context: '#my_chart',
      success: function (data) {
        var html = $(data);
        updated_data = $(data).find("#my_chart").attr("my_data");
        updated_data = JSON.parse( updated_data );
        $("#my_chart").replaceWith($(data).find("#my_chart"));
        generate_chart(updated_data);
        // $("#my_chart").replaceWith(("#my_chart", html));
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
