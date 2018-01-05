import $ from "jquery";
import jQuery from "jquery";
window.$ = $;
window.jQuery = jQuery;

require("noty");

require("bootstrap/dist/js/bootstrap.bundle.js");
require("bootstrap-datepicker/dist/js/bootstrap-datepicker");
require("bootstrap-slider/dist/bootstrap-slider");
let md = require("mdbootstrap");
require("jscrollpane");

$(document).ready(() => {
    $(".datepicker").datepicker({
        orientation: "bottom auto"
    });
    console.log("awfwafwf");


    let toTime = function(decimal) {
        let hrs = parseInt(Number(decimal));
        let min = Math.round((Number(decimal) - hrs) * 60);
        let am = true;
        if(hrs > 12) {
            hrs -= 12;
            am = false;
        }
        hrs = String(hrs);
        min = String(min);
        if (min.length === 1) min += "0";
        if(am) return hrs + ":" + min + " AM";
        else return hrs + ":" + min + " PM";
    };

    $(".request_slider, .conflict_slider").each(function () {
        $(this).slider({id: this.id, min: 8, max: 24, range: true, value: [10, 12], step: .25, handle: "square", tooltip: "hide"});
        $(this).on("slide", function(slideEvt) {
            $("#" + this.id + "_val_0").text(toTime(slideEvt.value[0]));
            $("#" + this.id + "_val_1").text(toTime(slideEvt.value[1]));
        });
    });
    console.log("awfwafwf");

    let ctxL = document.getElementById("lineChart").getContext("2d");
    new md.Chart(ctxL, {
        type: "line",
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
                {
                    label: "My First dataset",
                    fillColor: "rgba(220,220,220,0.2)",
                    strokeColor: "rgba(220,220,220,1)",
                    pointColor: "rgba(220,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: [65, 59, 80, 81, 56, 55, 40]
                },
                {
                    label: "My Second dataset",
                    fillColor: "rgba(151,187,205,0.2)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: [28, 48, 40, 19, 86, 27, 90]
                }
            ]
        },
        options: {
            responsive: true
        }
    });

    console.log("awfwafwf");
});
