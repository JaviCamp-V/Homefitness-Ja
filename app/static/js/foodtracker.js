let currentKCal= 0;
let currentCode = 0;
let currentFoodItem = "";
let currentServings = 0;
let currentCalorie=0;

let Total = 0;
let save = [];



window.addEventListener("load", function () {
    let search = document.querySelector("#search");
    let results = document.querySelector("#results");
    let calculate = document.querySelector("#calculate");
    let calResults = document.querySelector("#calResults");
    let calDIv = document.querySelector("#calculator");
    let BurnedSum = document.querySelector("#totalCals");
    let addTotal = document.querySelector("#addTotal2");
    let adder = document.querySelector("#addTOTOtal2");
    let divDB = document.querySelector("#totalCalsTODB");
    let saver = document.querySelector("#save");
    let servings=document.querySelector("#servings");
  
  
    search.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
          calDIv.style.display = "none";
          calResults.style.display = "none";
          addTotal.style.display = "none";

          results.style.display = "block";

        pharse = search.value;
        if (pharse.length > 2) {
          data = { query: pharse };
          fetch("/homefitness/food-tracker/search", {
            method: "POST", // or 'PUT'
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          })
            .then((response) => response.json())
            .then((data) => {
              results.innerHTML = "";
              console.log(data.text);
              console.log(data);

              if(data.hints.length==0){
                results.innerHTML = "No records found";
                return;    

              }
              for (var i = 0; i < data.hints.length; i++) {

                var card = document.createElement("div");
                card.setAttribute("class", "card");
                card.style.width =" 18rem";
                var img = document.createElement("img");
                img.setAttribute("class", "card-img-top");
                img.src=data.hints[i].food.image;
                var cardbody = document.createElement("div");
                cardbody.setAttribute("class", "card-body");
                var h5 = document.createElement("h5");
                h5.setAttribute("calss", "card-title");
                h5.innerHTML=data.hints[i].food.label;
                var p = document.createElement("p");
                p.setAttribute("class", "card-text");
                var link = document.createElement("a");
                link.setAttribute("class", "badge badge-light");
                link.setAttribute(
                  "onclick",
                  "calculator('" + JSON.stringify(data.hints[i]) + "');"
                );
                link.innerHTML="Select Item";
                p.innerHTML=parseFloat(data.hints[i].food.nutrients.ENERC_KCAL).toFixed(2) + " per Serving";
                cardbody.appendChild(h5)
                cardbody.appendChild(p)
                cardbody.appendChild(link)
                card.appendChild(img);
                card.appendChild(cardbody);
                results.appendChild(card);
                console.log(data.hints[i])
               ;
             /** 
                          <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="..." alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Card title</h5>
              <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
              <a href="#" class="btn btn-primary">Go somewhere</a>
            </div>
          </div>
          */
              }
              console.log(data);
            })
            .catch((error) => {
              console.error("Error:", error);
            });
        }
    }
    });

    calculate.addEventListener("click", function (element) {
      element.preventDefault();
      let s = parseInt(document.getElementById("servings").value) || 0;
      calorie=currentKCal*s;
      calorie = parseFloat(calorie).toFixed(2); //kcl to cl
      calResults.innerHTML = calorie.toString();
      if (calorie>0) {
        addTotal.style.display = "block";
        currentServings = s;
        currentCalorie=calorie;
      }
      
  

    });
    adder.addEventListener("click", function (element) {
      element.preventDefault();
      Total = parseFloat(Total) + parseFloat(currentCalorie);
      BurnedSum.innerHTML = "";
      BurnedSum.innerHTML = parseFloat(Total).toFixed(2);
      save.push({
        code: currentCode,
        ingredients: currentFoodItem,
        calories: currentCalorie,
      });


      currentCode = 0;
      currentServings = 0;
      currentCalorie = 0;
      currentKCal = 0;
      calDIv.style.display = "none";
      calResults.style.display = "none";
      addTotal.style.display = "none";
      search.value="";
      divDB.style.display = "block";


});
saver.addEventListener("click", function (element) {
  element.preventDefault();
  data = { "Food": save };
  fetch("/homefitness/food-tracker/save", {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Record save sucessfully");
      console.log(data);
      save = [];
      Total = 0;
      BurnedSum.innerHTML = parseFloat(Total).toFixed(2);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
  
     

});
function calculator(obj) {
  let result = JSON.parse(obj);
  console.log(result);
  results.innerHTML = "";
  document.getElementById("calculator").style.display = "block";
  document.getElementById("calResults").style.display = "block";
  document.getElementById("results").style.display = "none";
  document.getElementById("foodItem").value = result.food.label;
  document.getElementById("foodKcal").value =parseFloat(result.food.nutrients.ENERC_KCAL).toFixed(2);
  document.getElementById("servings").value = 0;

  


   currentKCal= result.food.nutrients.ENERC_KCAL;
   currentCode = result.food.foodId;
   currentFoodItem = result.food.label;
   currentServings = 0;
  
}

function imageExists(image_url){

  var http = new XMLHttpRequest();

  http.open('HEAD', image_url, false);
  http.send();

  return http.status != 404;

}