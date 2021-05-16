window.addEventListener("load", function () {
    let search = document.querySelector("#search");
    let results = document.querySelector("#results");
  
    search.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
      
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

              if(data.hints.length>0){

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
                link.innerHTML="Add to Total";
                p.innerHTML=data.hints[i].food.nutrients.ENERC_KCAL;
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


});

function imageExists(image_url){

  var http = new XMLHttpRequest();

  http.open('HEAD', image_url, false);
  http.send();

  return http.status != 404;

}