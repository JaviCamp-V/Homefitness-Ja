let currentMET=0;
let currentactivity="";

window.addEventListener('load', function() {

    let search = document.querySelector('#search');
    let results = document.querySelector('#results');
    let calculate = document.querySelector('#calculate');
    let edit = document.querySelector('#edit');
    let calResults = document.querySelector('#calResults');
    let calDIv = document.querySelector('#calculator');




    search.addEventListener("keyup", function (element) {
        calDIv.style.display = "none";
        calResults.style.display = "none";
        element.preventDefault();
        pharse=search.value;
        if (pharse.length>2){
                data={"query":pharse};
                fetch("/homefitness/caloriecalculator/search",{
                    method: 'POST', // or 'PUT'
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    }).then(response => response.json())
                    .then(data => {
                        results.innerHTML="";
                        if (data.results.length==0){
                            results.innerHTML="No records found";
                            return;
                        }
                         for(var i = 0; i < data.results.length ;i++){
                            //const btn = document.querySelector(".btn")
                            //console.log(data.results[i]);
                            result=data.results[i]
                            var p = document.createElement("p");

                            var link = document.createElement("a");
                            link.setAttribute("class","badge badge-light");
                            //link.addEventListener("click",function(){
                            //    currentMET=result.met;
                            //    currentactivity=result.activities;
                           // });
                            //link.setAttribute('href', "test("+JSON.stringify(result)+")");
                            link.setAttribute("onclick","calculator('"+JSON.stringify(result)+"');");
                            link.innerHTML = result.activities;
                            p.appendChild(link);
                            results.appendChild(p);

        
                         }
                        
                    })
                    .catch((error) => {
                        console.error('Error:', error);        
                });
         }
    });
     function test(values){
         alert(values);
     }
    calculate.addEventListener("click", function (element) {
        element.preventDefault();
        let age =document.getElementById('age').value;
        let weight =document.getElementById('weight').value;
        let height =document.getElementById('heightcm').value;
        let isMAle =document.getElementById('male').checked;
        let hr =parseInt(document.getElementById('hr').value) || 0;
        let min =parseInt(document.getElementById('min').value)|| 0;
        let BMR=0;
        if (isMAle){
           BMR= (13.75* (weight/2.2046)) + (5 *height) - (6.76 * age) + 66;
        }else{
            BMR=(9.56* (weight/2.2046)) + (1.85*height) - (4.68 * age) + 655;
        }

        let calorie = (currentMET/60) *(BMR/1440) * ((hr*60)+min);
        calorie=parseFloat((calorie*1000)).toFixed(2); //kcl to cl
        calResults.innerHTML=calorie.toString();



           /**
    Calorie Burn = (BMR / 24) x MET x T
    ///Calculator Formulas
   
    Calorie Burn = (BMR / 24) x MET x T


    For males: BMR = (13.75 x WKG) + (5 x HC) - (6.76 x age) + 66
     For females: BMR = (9.56 x WKG) + (1.85 x HC) - (4.68 x age) + 655

     (kcal burned) = (MET value) X (BMR/24) X (duration of activity in hours)

       (kcal burned) = (MET value/60) X (BMR/1440 minutes per day) X (duration of activity in minutes)
     */
    });
    edit.addEventListener("click", function (element) {
        element.preventDefault();
        document.getElementById('male').removeAttribute('disabled');
        document.getElementById('female').removeAttribute('disabled');
        document.getElementById('age').removeAttribute('readonly');
        document.getElementById('heightcm').removeAttribute('readonly');
        document.getElementById('weight').removeAttribute('readonly');
        document.getElementById('hr').value='';
        document.getElementById('min').value='';





    }); 




});

function calculator(obj){
    let result=JSON.parse(obj);
    console.log(result.met);
    currentMET=result.met; 
    currentactivity=result.activities;
    results.innerHTML="";
    document.getElementById("calculator").style.display = "block";
    document.getElementById("calResults").style.display = "block";

    document.getElementById('activity').value=result.activities;
}
