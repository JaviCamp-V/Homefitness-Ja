/* Add your Application JavaScript */

let exc_choice = document.querySelector(".exc-choice");
let correction_choice = document.querySelector(".correction-choice");
$(document).ready(function () {
  $("#select-exc li").on("click", function () {
    var txt = $(this).text();
    exc_choice.innerHTML = txt;
  });
});

$(document).ready(function () {
  $("#select-correction li").on("click", function () {
    var txt = $(this).text();
    correction_choice.innerHTML = txt;
  });
});
