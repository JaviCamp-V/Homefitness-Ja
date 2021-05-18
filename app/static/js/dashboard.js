window.addEventListener("load", function () {
  let lastsession = document.querySelector("#lastsession").getContext("2d");
  let canvas = document.querySelector("#lastsession");
  const compare = document.querySelector("#compare");
  const progress = document.querySelector("#progress").getContext("2d");
  const exercise = document.querySelector("#exercisetype");
  const calorieschart = document
    .querySelector("#calorieschart")
    .getContext("2d");
  const sessionhart = document.querySelector("#sessionhart").getContext("2d");
  const session = document.querySelector("#session");
  var chartone_Lables = [];
  var chartone_title = "Last exercise session";
  var chartone_data = [];
  var chartone_sid = -1;
  var chartone_type = "";
  var chartone = null;
  var charttwo_Lables = [];
  var charttwo_title = "Last exercise session";
  var charttwo_data = [];
  var charttwo_sid = -1;
  var charttwo_type = "";
  var charttwo = null;
  var chart3 = null;
  var chart4 = null;
  var chartfour_Lables = null;
  var chartfour_title = null;
  var chartfour_data = null;
  var chartfour_type = null;
  var chart5 = null;

  compare.style.display = "none";
  exercise.addEventListener("change", function (element) {
    element.preventDefault();

    console.log(exercise.value);
    chart5.destroy();
    chart4.destroy();
    charttwo.destroy();
    session.innerHTML = "";

    /**
     * Draw new sesion charts
     */
    fetch("/homefitness/dashboard/" + exercise.value + "/sessions/", {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.hasOwnProperty("Status")) {
          for (var i = 0; i < data.sessions.length; i++) {
            var x = document.createElement("OPTION");
            x.value = data.sessions[i].sid;
            x.text = data.sessions[i].label;
            session.appendChild(x);
          }

          fetch(
            "/homefitness/dashboard/" + exercise.value + "/" + session.value,
            {
              method: "GET", // or 'PUT'
              headers: {
                "Content-Type": "application/json",
              },
            }
          )
            .then((response) => response.json())
            .then((data) => {
              if (data.hasOwnProperty("Error")) {
                chartone_title = "No sessesion data is available";
              } else {
                chartfour_Lables = data.labels;
                chartfour_title = data.exercise;
                chartfour_data = data.data;
                chartfour_type = data.exercise;
              }
              chart5 = new Chart(sessionhart, {
                type: "doughnut",
                data: {
                  labels: chartfour_Lables,
                  datasets: [
                    {
                      label: chartfour_title,
                      data: chartfour_data,
                      backgroundColor: [
                        "rgb(255, 99, 132)",
                        "rgb(54, 162, 235)",
                      ],
                      hoverOffset: 4,
                    },
                  ],
                },
                options: {},
              });
            })
            .catch((error) => {
              console.error("Error:", error);
              chart5 = new Chart(sessionhart, {
                type: "doughnut",
                data: {
                  labels: chartfour_Lables,
                  datasets: [
                    {
                      label: chartfour_title,
                      data: chartfour_data,
                      backgroundColor: [
                        "rgb(255, 99, 132)",
                        "rgb(54, 162, 235)",
                      ],
                      hoverOffset: 4,
                    },
                  ],
                },
                options: {},
              });
            });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    //**redraw progress chart */
    fetch("/homefitness/dashboard/" + exercise.value, {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.hasOwnProperty("Error")) {
          charttwo_title = "No sessesion data is available";
        } else {
          charttwo_Lables = data.labels;
          charttwo_title = data.exercise;
          charttwo_data = data.data;
          charttwo_sid = data.sid;
          charttwo_type = data.exercise;
          if (charttwo_sid > 1) {
            compare.style.display = "block";
          }
        }
        charttwo = new Chart(progress, {
          type: "line",
          data: {
            labels: charttwo_Lables,
            datasets: [
              {
                label: charttwo_title,
                backgroundColor: "rgb(0,99,132)",
                borderColor: "rgb(0,99,132)",
                data: charttwo_data,
              },
            ],
          },
          options: {},
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        charttwo = new Chart(progress, {
          type: "line",
          data: {
            labels: "No sesdion data is available for user at this moment",
            datasets: [
              {
                label: charttwo_title,
                backgroundColor: "rgb(0,99,132)",
                borderColor: "rgb(0,99,132)",
                data: charttwo_data,
              },
            ],
          },
          options: {},
        });
      });
    //**redraw calorie chart */
    fetch("/homefitness/dashboard/" + exercise.value + "/calorie/", {
      method: "GET", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        if (data.hasOwnProperty("Error")) {
          chartone_title = "No sessesion data is available";
        } else {
          var chartthree_Lables = data.labels;
          var chartthree_title = data.exercise;
          var chartthree_data = data.data;
        }
        chart4 = new Chart(calorieschart, {
          type: "bar",
          data: {
            labels: chartthree_Lables,
            datasets: [
              {
                label: chartthree_title,
                backgroundColor: "rgb(0,99,132)",
                borderColor: "rgb(0,99,132)",
                data: chartthree_data,
              },
            ],
          },
          options: {},
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        var chartone = new Chart(lastsession, {
          type: "bar",
          data: {
            labels: "No sesdion data is available for user at this moment",
            datasets: [
              {
                label: [""],
                backgroundColor: "rgb(0,99,132)",
                borderColor: "rgb(0,99,132)",
                data: [0],
              },
            ],
          },
          options: {},
        });
      });
  });
  session.addEventListener("change", function (element) {
    element.preventDefault();

    console.log(exercise.value);
    chart5.destroy();
    fetch(
      "/homefitness/dashboard/" +
        exercise.value +
        "/" +
        parseInt(session.value),
      {
        method: "GET", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("session:", data);
        if (data.hasOwnProperty("Error")) {
          chartfour_title = "No sessesion data is available";
          chartfour_Lables = ["no data"];
          chartfour_data = [0];
        } else {
          chartfour_Lables = data.labels;
          chartfour_title = data.exercise;
          chartfour_data = data.data;
          console.log(chartfour_Lables);
        }
        chart5 = new Chart(sessionhart, {
          type: "doughnut",
          data: {
            labels: chartfour_Lables,
            datasets: [
              {
                label: chartfour_title,
                data: chartfour_data,
                backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                hoverOffset: 4,
              },
            ],
          },
          options: {},
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        chart5 = new Chart(sessionhart, {
          type: "doughnut",
          data: {
            labels: [""],
            datasets: [
              {
                label: ["no data"],
                data: [0],
                backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                hoverOffset: 4,
              },
            ],
          },
          options: {},
        });
      });
  });

  fetch("/homefitness/dashboard/lastsession", {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      if (data.hasOwnProperty("Error")) {
        chartone_Lables = [];
        chartone_title = [];
        chartone_data = [];
        chartone_sid = [];
        chartone_type = [];
        // chartone_title = "No sessesion data is available";
      } else {
        chartone_Lables = data.labels;
        chartone_title = data.exercise;
        chartone_data = data.data;
        chartone_sid = data.sid;
        chartone_type = data.exercise;
        if (chartone_sid > 1) {
          compare.style.display = "block";
        }
      }
      chartone = new Chart(lastsession, {
        type: "bar",
        data: {
          labels: chartone_Lables,
          datasets: [
            {
              label: chartone_title,
              backgroundColor: "rgb(0,99,132)",
              borderColor: "rgb(0,99,132)",
              data: chartone_data,
            },
          ],
        },
        options: {},
      });
    })
    .catch((error) => {
      console.error("Error:", error);
      var chartone = new Chart(lastsession, {
        type: "bar",
        data: {
          labels: "No sesdion data is available for user at this moment",
          datasets: [
            {
              label: chartone_title,
              backgroundColor: "rgb(0,99,132)",
              borderColor: "rgb(0,99,132)",
              data: chartone_data,
            },
          ],
        },
        options: {},
      });
    });

  /***
   * progress fetch and graphing function
   */
  fetch("/homefitness/dashboard/" + exercise.value, {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("progess:", data);
      if (data.hasOwnProperty("Error")) {
        charttwo_title = "No sessesion data is available";
      } else {
        charttwo_Lables = data.labels;
        charttwo_title = data.exercise;
        charttwo_data = data.data;
        charttwo_sid = data.sid;
        charttwo_type = data.exercise;
        if (charttwo_sid > 1) {
          compare.style.display = "block";
        }
      }
      charttwo = new Chart(progress, {
        type: "line",
        data: {
          labels: charttwo_Lables,
          datasets: [
            {
              label: charttwo_title,
              backgroundColor: "rgb(0,99,132)",
              borderColor: "rgb(0,99,132)",
              data: charttwo_data,
            },
          ],
        },
        options: {},
      });
    })
    .catch((error) => {
      console.error("Error:", error);
      charttwo = new Chart(progress, {
        type: "line",
        data: {
          labels: "No sesdion data is available for user at this moment",
          datasets: [
            {
              label: charttwo_title,
              backgroundColor: "rgb(0,99,132)",
              borderColor: "rgb(0,99,132)",
              data: charttwo_data,
            },
          ],
        },
        options: {},
      });
    });

  ///***   calorie chart ***/

  fetch("/homefitness/dashboard/" + exercise.value + "/calorie/", {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      if (data.hasOwnProperty("Error")) {
        chartone_title = "No sessesion data is available";
      } else {
        var chartthree_Lables = data.labels;
        var chartthree_title = data.exercise;
        var chartthree_data = data.data;
      }
      chart4 = new Chart(calorieschart, {
        type: "bar",
        data: {
          labels: chartthree_Lables,
          datasets: [
            {
              label: chartthree_title,
              backgroundColor: "rgb(0,99,132)",
              borderColor: "rgb(0,99,132)",
              data: chartthree_data,
            },
          ],
        },
        options: {},
      });
    })
    .catch((error) => {
      console.error("Error:", error);
      var chartone = new Chart(lastsession, {
        type: "bar",
        data: {
          labels: "No sesdion data is available for user at this moment",
          datasets: [
            {
              label: [""],
              backgroundColor: "rgb(0,99,132)",
              borderColor: "rgb(0,99,132)",
              data: [0],
            },
          ],
        },
        options: {},
      });
    });

  ///***   sessionhart chart ***/

  fetch("/homefitness/dashboard/" + exercise.value + "/sessions/", {
    method: "GET", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      if (data.hasOwnProperty("Status")) {
        for (var i = 0; i < data.sessions.length; i++) {
          console.log(data.sessions[i]);
          var x = document.createElement("OPTION");
          x.value = data.sessions[i].sid;
          x.text = data.sessions[i].label;
          session.appendChild(x);
        }

        fetch(
          "/homefitness/dashboard/" + exercise.value + "/" + session.value,
          {
            method: "GET", // or 'PUT'
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
          .then((response) => response.json())
          .then((data) => {
            console.log("helloworld:", data);
            if (data.hasOwnProperty("Error")) {
              chartone_title = "No sessesion data is available";
            } else {
              chartfour_Lables = data.labels;
              chartfour_title = data.exercise;
              chartfour_data = data.data;
              chartfour_type = data.exercise;
              console.log(chartfour_Lables);
            }
            chart5 = new Chart(sessionhart, {
              type: "doughnut",
              data: {
                labels: chartfour_Lables,
                datasets: [
                  {
                    label: chartfour_title,
                    data: chartfour_data,
                    backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                    hoverOffset: 4,
                  },
                ],
              },
              options: {
                legend: {
                  position: "bottom",
                },
              },
            });
          })
          .catch((error) => {
            console.error("Error:", error);
            chart5 = new Chart(sessionhart, {
              type: "doughnut",
              data: {
                labels: chartfour_Lables,
                datasets: [
                  {
                    label: chartfour_title,
                    data: chartfour_data,
                    backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
                    hoverOffset: 4,
                  },
                ],
              },
              options: {
                legend: {
                  position: "bottom",
                },
              },
            });
          });
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  compare.addEventListener("click", function (element) {
    element.preventDefault();
    compare.disabled = true;
    compare.classList.remove("btn-primary");
    compare.classList.add("btn-success");

    chartone.destroy();
    let url =
      "/homefitness/dashboard/" +
      chartone_type +
      "/" +
      (parseInt(chartone_sid) - 1).toString();
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        if (data.hasOwnProperty("Error")) {
          chartone_title = "No data";
          chartone_Lables = [];
        } else {
          chartone_title = data.exercise;
          chartone_dataC = data.data;
          chartone_sid_C = data.sid;
        }
        chartone = new Chart(lastsession, {
          type: "bar",
          data: {
            labels: chartone_Lables,
            datasets: [
              {
                label: chartone_sid,
                backgroundColor: "rgb(0,99,132)",
                //borderColor: 'rgb(0,99,132)',
                data: chartone_data,
              },
              {
                label: chartone_sid_C,
                backgroundColor: "rgb(200,0,0)",
                //borderColor: 'rgb(0,99,132)',
                data: chartone_dataC,
              },
            ],
          },
          options: {
            legend: {
              position: "bottom",
            },
          },
        });
      })
      .catch((error) => {
        console.error("Error:", error);
        var chartone = new Chart(lastsession, {
          type: "bar",
          data: {
            labels: "No sesdion data is available for user at this moment",
            datasets: [
              {
                label: chartone_title,
                backgroundColor: "rgb(0,99,132)",
                borderColor: "rgb(0,99,132)",
                data: chartone_data,
              },
            ],
          },
          options: {
            legend: {
              position: "bottom",
            },
          },
        });
      });
  });
});
