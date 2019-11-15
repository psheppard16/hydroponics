import $ from "jquery";
import jQuery from "jquery";

window.$ = $;
window.jQuery = jQuery;

import {Global} from "./global.js";

$(document).ready(function () {
    "use strict";

    new Global();
});
