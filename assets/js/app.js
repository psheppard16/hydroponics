import $ from "jquery";
import jQuery from "jquery";
window.$ = $;
window.jQuery = jQuery;

require("noty");

require("bootstrap/dist/js/bootstrap.bundle.js");
require("bootstrap-datepicker/dist/js/bootstrap-datepicker");
require("bootstrap-slider/dist/bootstrap-slider");

require("jscrollpane");

$(document).ready(() => {
    $(".datepicker").datepicker({
        orientation: "bottom auto"
    });


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
});
