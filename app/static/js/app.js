/* Add your Application JavaScript */

let exc_choice = document.querySelector(".exc-choice");
let correction_choice = document.querySelector(".correction-choice");
let exc_video = document.querySelector(".exc-video");

$(document).ready(function () {
  $("#select-exc li").on("click", function () {
    var txt = $(this).text();
    exc_choice.innerHTML = txt + " Selected";
  });
});
