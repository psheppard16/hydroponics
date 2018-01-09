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
    //initialize datepicker ex.
    // $(".datepicker").datepicker({
    //     orientation: "bottom auto"
    // });

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

    $(".data-slider").each(function () {
        $(this).slider({id: this.id, range: true, handle: "square", tooltip: "hide"});
        $(this).on("slide", function(slideEvt) {
            let val_1 = $("#" + "id_low_" + this.id.split("_")[1]);
            let val_2 = $("#" + "id_high_" + this.id.split("_")[1]);
            val_1.attr("value", slideEvt.value[0]);
            val_2.attr("value", slideEvt.value[1]);
        });
    });
});
