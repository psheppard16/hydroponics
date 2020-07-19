import $ from "jquery";
import jQuery from "jquery";

window.$ = $;
window.jQuery = jQuery;

require("bootstrap");
require("bootstrap-slider");
require("chosen-js");

let Chart = require("chart.js");

//slider helper method
export let toTime = (decimal) => {
    let hrs = parseInt(Number(decimal));
    let min = Math.round((Number(decimal) - hrs) * 60);
    let am = true;
    if (hrs >= 12 && hrs < 24) am = false;
    if (hrs > 12) hrs -= 12;
    hrs = String(hrs);
    min = String(min);
    if (min.length === 1) min += "0";
    if (am) return hrs + ":" + min + " AM";
    return hrs + ":" + min + " PM";
};

export let init_data_chart = () => {
    let options = {
        scales: {
            xAxes: [{
                id: "x-axis",
                type: "time"
            }]
        }
    };
    //graph initialization
    $("#pHLineChart").each(function (index, chart) {
        $.ajax({
            url: "/hydro/api/data", success: function (data) {
                let pH_data = [];
                let pH_labels = [];
                for (let i = 0; i < data.length; i++) {
                    let info = data[i];
                    let date = Date.parse(info["date_time"]);
                    if (date > Date.now() - 1000 * 60 * 60 * 24) {
                        if (info["type"] === 1) {
                            pH_data.push(data[i]["value"]);
                            pH_labels.push(date);
                        }
                    }
                }
                new Chart(chart, {
                    type: "line",
                    data: {
                        labels: pH_labels,
                        datasets: [{
                            data: pH_data,
                            label: "pH",
                            borderColor: "#3e95cd",
                            fill: false
                        }]
                    },
                    options: options
                });
            }
        });
    });
    $("#ecLineChart").each(function (index, chart) {
        $.ajax({
            url: "/hydro/api/data", success: function (data) {
                let ec_data = [];
                let ec_labels = [];
                for (let i = 0; i < data.length; i++) {
                    let info = data[i];
                    let date = Date.parse(info["date_time"]);
                    if (date > Date.now() - 1000 * 60 * 60 * 24) {
                        if (info["type"] === 2) {
                            ec_data.push(data[i]["value"]);
                            ec_labels.push(date);
                        }
                    }
                }
                new Chart(chart, {
                    type: "line",
                    data: {
                        labels: ec_labels,
                        datasets: [{
                            data: ec_data,
                            label: "EC",
                            borderColor: "#8e5ea2",
                            fill: false
                        }]
                    },
                    options: options
                });
            }
        });
    });
    $("#orpLineChart").each(function (index, chart) {
        $.ajax({
            url: "/hydro/api/data", success: function (data) {
                let orp_data = [];
                let orp_labels = [];
                for (let i = 0; i < data.length; i++) {
                    let info = data[i];
                    let date = Date.parse(info["date_time"]);
                    if (date > Date.now() - 1000 * 60 * 60 * 24) {
                        if (info["type"] === 3) {
                            orp_data.push(data[i]["value"]);
                            orp_labels.push(date);
                        }
                    }
                }
                new Chart(chart, {
                    type: "line",
                    data: {
                        labels: orp_labels,
                        datasets: [{
                            data: orp_data,
                            label: "ORP",
                            borderColor: "#8e5ea2",
                            fill: false
                        }]
                    },
                    options: options
                });
            }
        });
    });
    $("#temperatureLineChart").each(function (index, chart) {
        $.ajax({
            url: "/hydro/api/data", success: function (data) {
                let temperature_data = [];
                let temperature_labels = [];
                for (let i = 0; i < data.length; i++) {
                    let info = data[i];
                    let date = Date.parse(info["date_time"]);
                    if (date > Date.now() - 1000 * 60 * 60 * 24) {
                        if (info["type"] === 4) {
                            temperature_data.push(data[i]["value"]);
                            temperature_labels.push(date);
                        }
                    }
                }
                new Chart(chart, {
                    type: "line",
                    data: {
                        labels: temperature_labels,
                        datasets: [{
                            data: temperature_data,
                            label: "Temperature",
                            borderColor: "#e8c3b9",
                            fill: false
                        }
                        ]
                    },
                    options: options
                });
            }
        });
    });
};