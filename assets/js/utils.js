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
    if(hrs >= 12 && hrs < 24) am = false;
    if(hrs > 12) hrs -= 12;
    hrs = String(hrs);
    min = String(min);
    if (min.length === 1) min += "0";
    if(am) return hrs + ":" + min + " AM";
    return hrs + ":" + min + " PM";
};

export let init_data_chart = () => {
    //graph initialization
    $(".analytics_chart").each(function(index, chart) {
        $.ajax({
            url: "/timeclock/api/employees", success: function (employees) {
                let data_array = [];
                let label_array = [];
                for (let i = 0; i < employees.length; i++) {
                    let employee = employees[i];
                    if (employee["office"] && employee["clocked_in"]) { //make sure that the employee has an office and is clocked in
                        if (!label_array.includes(employee["office"])) { //only add the office to labels if it is not present
                            label_array.push(employee["office"]);
                            data_array.push(0);
                        }
                        data_array[label_array.indexOf(employee["office"])] += 1; //add 1 to the employee count for that office
                    }
                }
                new Chart(chart, {
                    type: "bar",
                    data: {
                        labels: label_array,
                        datasets: [{
                            label: "# of Employees",
                            data: data_array,
                            backgroundColor: [
                                "rgba(255, 99, 132, 0.75)",
                                "rgba(255, 99, 132, 0.75)",
                                "rgba(255, 99, 132, 0.75)",
                                "rgba(255, 99, 132, 0.75)",
                            ],
                            borderColor: [
                                "rgba(255,99,132,1)",
                                "rgba(255,99,132,1)",
                                "rgba(255,99,132,1)",
                                "rgba(255,99,132,1)",
                            ],
                            borderWidth: 2
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true,
                                    stepSize: 1
                                }
                            }]
                        },
                        layout: {
                            padding: {
                                left: 0,
                                right: 0,
                                top: 15,
                                bottom: 15
                            }
                        }
                    }
                });
            }
        });
    });
};