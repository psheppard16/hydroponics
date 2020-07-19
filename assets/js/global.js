import $ from "jquery";
import jQuery from "jquery";

window.$ = $;
window.jQuery = jQuery;

require("bootstrap");
require("bootstrap-slider");
require("chosen-js");

window.moment = require("moment");
require("tempusdominus-bootstrap-4");

import * as utils from "./utils.js";

export class Global {
    constructor() {
        this._set_events();
        this._init();
    }

    _set_events() {

    }

    _init() {
        utils.init_data_chart();

        // datepicker initialization
        $(".type-date").datetimepicker({format: "MM/DD/YYYY"});
        $(".type-datetime").datetimepicker({format: "MM/DD/YYYY h:mm A"});
        $(".type-time").datetimepicker({format: "HH:mm:ss", inline: true, sideBySide: true});

        // chosen initialization
        $(".chosen-select").chosen({width: "100%"});
        $(".chosen-select-half").chosen({width: "50%"});
        $(".chosen-select-third").chosen({width: "33%"});

        //slider initialization
        $(".data-slider").each(function () {
            $(this).slider({id: this.id, range: true, handle: "square", tooltip: "hide"});
            $(this).on("slide", function (slideEvt) {
                $("#id_low_" + this.id.split("_")[1]).val(slideEvt.value[0]);
                console.log("#id_low_" + this.id.split("_")[1]);
                $("#id_high_" + this.id.split("_")[1]).val(slideEvt.value[1]);
            });
        });
        $(".time_slider").each(function () {
            $(this).slider();
            $(this).on("slide", function (slideEvt) {
                $("#id_label_0_" + this.id.split("_")[2]).val(utils.toTime(slideEvt.value[0]));
                $("#id_label_1_" + this.id.split("_")[2]).val(utils.toTime(slideEvt.value[1]));
            });
        });
        $(".readonly_slider").slider({enabled: false});
    }
}